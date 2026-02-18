"""In-memory run history store."""

from dataclasses import dataclass, field


@dataclass
class MemoryStore:
    events: list[dict] = field(default_factory=list)

    def append(self, event: dict) -> None:
        self.events.append(event)

    def all(self) -> list[dict]:
        return list(self.events)
