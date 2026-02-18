"""Typed runtime settings."""

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TradingConfig(BaseModel):
    """Trading-specific controls."""

    exchange: str = "Binance AUS"
    symbol: str = "BTCUSDT"
    max_daily_loss_usd: float = 20.0
    paper_trading: bool = True


class Settings(BaseSettings):
    """Top-level app settings loaded from environment."""

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__", extra="ignore")

    app_name: str = "bitcoin-test-agent"
    environment: str = "dev"
    runtime_language: str = "python"
    cloud_llm_provider: str = "openai"
    openai_api_key: str = Field(default="", repr=False)
    openai_model: str = "gpt-4.1-mini"
    dashboard_enabled: bool = True
    trading: TradingConfig = TradingConfig()


settings = Settings()
