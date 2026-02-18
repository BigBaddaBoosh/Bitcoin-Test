"""Single-run autonomous loop scaffold."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from agent_core.llm_gateway import LLMGateway
from memory.store import MemoryStore


@dataclass
class AgentRunLoop:
    llm: LLMGateway
    memory: MemoryStore

    def run_once(self, objective: str) -> dict:
        run_id = datetime.now(UTC).strftime("run-%Y%m%d%H%M%S")
        plan = self.llm.generate_plan(objective)
        self.memory.append({"run_id": run_id, "stage": "plan", "value": plan})

        review = self.llm.critic_review(plan, objective)
        self.memory.append({"run_id": run_id, "stage": "review", "value": review})

        return {
            "run_id": run_id,
            "objective": objective,
            "plan": plan,
            "review": review,
            "events": self.memory.all(),
        }
