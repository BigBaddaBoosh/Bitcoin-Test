from pathlib import Path

from agent_core.settings import TradingConfig
from policy.engine import PolicyEngine
from trading.engine import TradeIntent, TradingEngine


def test_shell_allowlist_blocks_dangerous_commands() -> None:
    policy = PolicyEngine(workspace_root=Path.cwd())
    denied = policy.authorize_shell("rm -rf /")
    assert denied.allowed is False


def test_trade_risk_is_enforced() -> None:
    policy = PolicyEngine(workspace_root=Path.cwd())
    engine = TradingEngine(
        config=TradingConfig(exchange="Binance AUS", symbol="BTCUSDT", max_daily_loss_usd=20.0),
        policy=policy,
    )

    accepted, _ = engine.evaluate_intent(
        TradeIntent(side="buy", quantity_btc=0.001, price_usd=60000, risk_usd=10)
    )
    assert accepted is True

    rejected, reason = engine.evaluate_intent(
        TradeIntent(side="buy", quantity_btc=0.001, price_usd=60000, risk_usd=25)
    )
    assert rejected is False
    assert "exceeds" in reason
