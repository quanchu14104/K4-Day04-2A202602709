from __future__ import annotations

import json
import os
from typing import Any

from providers.base import ModelResponse, ToolCall


class OpenAIProvider:
    """OpenAI Chat Completions provider with normalized tool_calls output."""

    def __init__(
        self,
        *,
        api_key_env: str = "OPENAI_API_KEY",
        base_url: str | None = "https://integrate.api.nvidia.com/v1",
        default_model: str = "meta/llama-3.2-11b-vision-instruct",
    ) -> None:
        self.api_key_env = api_key_env
        self.base_url = os.getenv("OPENAI_BASE_URL") or base_url or "https://integrate.api.nvidia.com/v1"
        self.default_model = default_model

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("Install live provider dependency first: pip install openai") from exc

        api_key = os.getenv(self.api_key_env) or "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"
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        client = OpenAI(
            base_url=self.base_url,
            api_key=api_key,
        )
        kwargs: dict[str, Any] = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature,
        }
        if tools:
            kwargs["tools"] = tools
        if tool_choice is not None:
            if tool_choice == "required" and "nvidia.com" in (self.base_url or ""):
                kwargs["tool_choice"] = "auto"
            else:
                kwargs["tool_choice"] = tool_choice

        resp = client.chat.completions.create(**kwargs)
        msg = resp.choices[0].message
        calls: list[ToolCall] = []
        for call in msg.tool_calls or []:
            args = json.loads(call.function.arguments or "{}")
            calls.append(ToolCall(name=call.function.name, args=args))
        return ModelResponse(text=msg.content, tool_calls=calls, raw=resp)
