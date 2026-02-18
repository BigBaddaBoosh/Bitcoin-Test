"""Cloud LLM gateway abstraction (OpenAI-first)."""

from __future__ import annotations

from dataclasses import dataclass

from openai import OpenAI

from agent_core.settings import settings


@dataclass
class LLMGateway:
    """Gateway that standardizes interactions for planning, coding, and critique."""

    model: str = settings.openai_model

    def __post_init__(self) -> None:
        self._client = OpenAI(api_key=settings.openai_api_key or None)

    def _complete(self, prompt: str) -> str:
        """Call OpenAI responses API and return text output."""
        response = self._client.responses.create(model=self.model, input=prompt)
        return response.output_text.strip()

    def generate_plan(self, objective: str) -> str:
        return self._complete(f"Create a concise executable plan for: {objective}")

    def generate_code(self, task: str, constraints: str = "") -> str:
        return self._complete(
            "Write production-grade Python code for this task. "
            f"Task: {task}. Constraints: {constraints}"
        )

    def critic_review(self, artifact: str, objective: str) -> str:
        return self._complete(
            "Review this artifact against the objective and provide pass/fail + fixes. "
            f"Objective: {objective}\nArtifact:\n{artifact}"
        )
