from pydantic import BaseSettings

class Config(BaseSettings):
    EXCHANGE_ID: str
    TIMEFRAME: str = '1h'
    NUM_CANDLES: int = 24
    PRICE_THRESHOLD: float = 5.0
    VOLUME_THRESHOLD_PERCENT: float = 200.0
    VOLATILITY_THRESHOLD: float = 0.1
    FUNDING_RATE_THRESHOLD: float = 0.01
    LIQUIDATION_THRESHOLD: float = 1000000.0
    CHECK_INTERVAL: int = 60

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

