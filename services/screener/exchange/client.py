import ccxt.async_support as ccxt
from ..config import Config

class ExchangeClient:
    def __init__(self, config: Config):
        self.exchange = getattr(ccxt, config.EXCHANGE_ID)()

    async def fetch_tickers(self):
        return await self.exchange.fetch_tickers()

    async def fetch_ohlcv(self, symbol: str, timeframe: str, since: int, limit: int):
        return await self.exchange.fetch_ohlcv(symbol, timeframe, since, limit)

    async def fetch_funding_rates(self):
        return await self.exchange.fetch_funding_rates()

    async def close(self):
        await self.exchange.close()

