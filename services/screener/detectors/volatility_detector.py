from typing import List, Dict
from ..exchange.client import ExchangeClient
from ..config import Config

class VolatilityDetector:
    def __init__(self, client: ExchangeClient, config: Config):
        self.client = client
        self.config = config

    async def screen_volatility(self) -> List[Dict]:
        tickers = await self.client.fetch_tickers()
        high_volatility_assets = []

        for symbol, ticker in tickers.items():
            if ticker['high'] and ticker['low']:
                volatility = (ticker['high'] - ticker['low']) / ticker['low']
                if volatility > self.config.VOLATILITY_THRESHOLD:
                    high_volatility_assets.append({
                        'symbol': symbol,
                        'volatility': volatility,
                        'current_price': ticker['last'],
                        'volume': ticker['quoteVolume']
                    })

        return sorted(high_volatility_assets, key=lambda x: x['volatility'], reverse=True)

