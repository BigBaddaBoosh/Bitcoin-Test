"""Policy checks for tool and trading actions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PolicyDecision:
    allowed: bool
    reason: str


@dataclass
class PolicyEngine:
    """Simple allowlist policy."""

    workspace_root: Path
    allowed_commands: tuple[str, ...] = ("python", "pytest", "pip", "uvicorn", "mkdir", "cat", "echo")

    def authorize_shell(self, command: str) -> PolicyDecision:
        token = command.strip().split()[0] if command.strip() else ""
        if token in self.allowed_commands:
            return PolicyDecision(True, "command allowed")
        return PolicyDecision(False, f"command '{token}' is not allowlisted")

    def authorize_path(self, path: Path) -> PolicyDecision:
        resolved = path.resolve()
        if self.workspace_root.resolve() in resolved.parents or resolved == self.workspace_root.resolve():
            return PolicyDecision(True, "path allowed")
        return PolicyDecision(False, "path outside workspace")

    def authorize_trade(self, requested_risk_usd: float, max_daily_loss_usd: float) -> PolicyDecision:
        if requested_risk_usd <= max_daily_loss_usd:
            return PolicyDecision(True, "trade risk within limit")
        return PolicyDecision(False, "trade rejected: requested risk exceeds max daily loss")
