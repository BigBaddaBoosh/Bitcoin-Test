"""FastAPI service entrypoint."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent_core.llm_gateway import LLMGateway
from agent_core.run_loop import AgentRunLoop
from agent_core.settings import settings
from memory.store import MemoryStore
from policy.engine import PolicyEngine
from trading.engine import TradeIntent, TradingEngine

app = FastAPI(title=settings.app_name)


class RunRequest(BaseModel):
    objective: str


class TradeRequest(BaseModel):
    side: str
    quantity_btc: float
    price_usd: float
    risk_usd: float


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "provider": settings.cloud_llm_provider,
        "exchange": settings.trading.exchange,
        "symbol": settings.trading.symbol,
        "max_daily_loss_usd": settings.trading.max_daily_loss_usd,
        "dashboard_enabled": settings.dashboard_enabled,
    }


@app.post("/agent/run")
def run_agent(payload: RunRequest) -> dict:
    if not settings.openai_api_key:
        raise HTTPException(status_code=400, detail="OPENAI_API_KEY is not configured")

    loop = AgentRunLoop(llm=LLMGateway(), memory=MemoryStore())
    return loop.run_once(payload.objective)


@app.post("/trade/intent")
def evaluate_trade(payload: TradeRequest) -> dict:
    policy = PolicyEngine(workspace_root=Path.cwd())
    engine = TradingEngine(config=settings.trading, policy=policy)
    accepted, reason = engine.evaluate_intent(
        TradeIntent(
            side=payload.side,
            quantity_btc=payload.quantity_btc,
            price_usd=payload.price_usd,
            risk_usd=payload.risk_usd,
        )
    )
    return {"accepted": accepted, "reason": reason}
