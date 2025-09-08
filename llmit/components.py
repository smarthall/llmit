from haystack import component
from haystack.dataclasses import ChatMessage
from haystack.core.component.types import Variadic
from typing import List, Dict, Any

@component()
class MessageCollector:
    def __init__(self):
        self._messages = []

    @component.output_types(messages=List[ChatMessage])
    def run(self, messages: Variadic[List[ChatMessage]]) -> Dict[str, Any]:
        self._messages.extend([msg for inner in messages for msg in inner])

        return {"messages": self._messages}

    def clear(self):
        self._messages = []
