import os

from typing import List
from haystack import Pipeline
from haystack.utils import Secret
from haystack.tools import Toolset
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.builders.chat_prompt_builder import ChatPromptBuilder
from haystack.components.routers import ConditionalRouter
from haystack.components.tools import ToolInvoker
from haystack.dataclasses import ChatMessage

from .tools import GitTools
from .components import MessageCollector
from .prompt import prompt_builder

routes = [
    {
        "condition": "{{replies[0].tool_calls | length > 0}}",
        "output": "{{replies}}",
        "output_name": "there_are_tool_calls",
        "output_type": List[ChatMessage],
    },
    {
        "condition": "{{replies[0].tool_calls | length == 0}}",
        "output": "{{replies}}",
        "output_name": "final_replies",
        "output_type": List[ChatMessage],
    },
]


def make_pipeline(tools: Toolset):
    pipeline = Pipeline()

    generator = OpenAIChatGenerator(
        api_key=Secret.from_env_var("LLMIT_API_KEY"),
        api_base_url=os.environ.get("LLMIT_API_BASE_URI"),
        model=os.environ.get("LLMIT_MODEL"),
        tools=tools,
    )

    # Components
    pipeline.add_component("message_collector", MessageCollector())
    pipeline.add_component("prompt_builder", prompt_builder)
    pipeline.add_component("generator", generator)
    pipeline.add_component("router", ConditionalRouter(routes=routes, unsafe=True))
    pipeline.add_component("tool_invoker", ToolInvoker(tools=tools, max_workers=1))

    # Connections
    pipeline.connect("prompt_builder", "message_collector")
    pipeline.connect("message_collector", "generator.messages")
    pipeline.connect("generator.replies", "router")
    pipeline.connect("router.there_are_tool_calls", "tool_invoker.messages")
    pipeline.connect("router.there_are_tool_calls", "message_collector")
    pipeline.connect("tool_invoker.tool_messages", "message_collector")

    return pipeline
