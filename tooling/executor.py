"""Local tool executor with policy enforcement."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from policy.engine import PolicyEngine, PolicyDecision


@dataclass
class ToolResult:
    ok: bool
    output: str


@dataclass
class ToolExecutor:
    workspace_root: Path
    policy: PolicyEngine

    def run_shell(self, command: str, timeout_s: int = 60) -> ToolResult:
        decision: PolicyDecision = self.policy.authorize_shell(command)
        if not decision.allowed:
            return ToolResult(False, decision.reason)

        proc = subprocess.run(
            command,
            shell=True,
            cwd=self.workspace_root,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        text = (proc.stdout or "") + (proc.stderr or "")
        return ToolResult(proc.returncode == 0, text.strip())

    def write_file(self, relative_path: str, content: str) -> ToolResult:
        file_path = self.workspace_root / relative_path
        decision = self.policy.authorize_path(file_path)
        if not decision.allowed:
            return ToolResult(False, decision.reason)

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return ToolResult(True, f"wrote {relative_path}")

    def read_file(self, relative_path: str) -> ToolResult:
        file_path = self.workspace_root / relative_path
        decision = self.policy.authorize_path(file_path)
        if not decision.allowed:
            return ToolResult(False, decision.reason)
        if not file_path.exists():
            return ToolResult(False, "file does not exist")
        return ToolResult(True, file_path.read_text())
