import ccxt.async_support as ccxt

class MultiExchangeClient:
    def __init__(self, exchange_ids):
        self.exchanges = {ex_id: getattr(ccxt, ex_id)() for ex_id in exchange_ids}

    async def fetch_tickers(self, exchange_id):
        return await self.exchanges[exchange_id].fetch_tickers()

    async def fetch_ohlcv(self, exchange_id, symbol, timeframe, limit):
        return await self.exchanges[exchange_id].fetch_ohlcv(symbol, timeframe, limit=limit)

    async def close(self):
        for exchange in self.exchanges.values():
            await exchange.close()

