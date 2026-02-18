"""Trading workflow scaffold (paper-first)."""

from dataclasses import dataclass

from agent_core.settings import TradingConfig
from policy.engine import PolicyEngine


@dataclass
class TradeIntent:
    side: str
    quantity_btc: float
    price_usd: float
    risk_usd: float


@dataclass
class TradingEngine:
    config: TradingConfig
    policy: PolicyEngine

    def evaluate_intent(self, intent: TradeIntent) -> tuple[bool, str]:
        decision = self.policy.authorize_trade(intent.risk_usd, self.config.max_daily_loss_usd)
        if not decision.allowed:
            return False, decision.reason
        return True, f"paper order accepted on {self.config.exchange} for {self.config.symbol}"
