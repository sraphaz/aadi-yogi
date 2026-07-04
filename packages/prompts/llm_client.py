from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass


DEFAULT_MODEL = os.environ.get("AADI_YOGI_LLM_MODEL", "gpt-4o-mini")
DEFAULT_BASE_URL = os.environ.get("AADI_YOGI_LLM_BASE_URL", "https://api.openai.com/v1")
DEFAULT_API_KEY = os.environ.get("AADI_YOGI_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")


@dataclass(frozen=True)
class LLMResponse:
    content: str
    provider: str
    model: str


class LLMClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or DEFAULT_API_KEY
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.model = model or DEFAULT_MODEL
        self.timeout = timeout

    @property
    def available(self) -> bool:
        return bool(self.api_key)

    def complete(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        if not self.available:
            raise RuntimeError("LLM API key not configured.")
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.4,
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "AadiYogiAgent/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed ({exc.code}): {detail}") from exc

        content = body["choices"][0]["message"]["content"].strip()
        return LLMResponse(content=content, provider="openai_compatible", model=self.model)
