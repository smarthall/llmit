from dotenv import load_dotenv

load_dotenv()

import logging

from cyclopts import App
from haystack import tracing
from haystack.tracing.logging_tracer import LoggingTracer

from .pipeline import make_pipeline
from .tools import GitTools

app = App()


@app.default
def run(
    repo: str,
    revision: str,
    tone: str = "Professional",
    language: str = "English",
    emoji: bool = True,
):
    logging.basicConfig(
        format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
    )
    logging.getLogger("haystack").setLevel(logging.DEBUG)

    tracing.tracer.is_content_tracing_enabled = (
        True  # to enable tracing/logging content (inputs/outputs)
    )
    tracing.enable_tracing(
        LoggingTracer(
            tags_color_strings={
                "haystack.component.input": "\x1b[1;31m",
                "haystack.component.name": "\x1b[1;34m",
            }
        )
    )

    print(f"Running llmit for {repo}")

    git_tools = GitTools(repo)

    pipeline = make_pipeline(git_tools.get_toolset())

    log = git_tools.get_revision_log_summary(revision)

    results = pipeline.run(
        {
            "prompt_builder": {
                "log_summary": log,
                "ref": revision,
                "tone": tone,
                "language": language,
                "emoji": emoji,
            },
        },
    )

    print(results["router"]["final_replies"][0].text)
