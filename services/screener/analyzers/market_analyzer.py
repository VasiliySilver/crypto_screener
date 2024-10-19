from typing import List, Dict
from ..exchange.client import ExchangeClient
from ..config import Config

class MarketAnalyzer:
    def __init__(self, client: ExchangeClient, config: Config):
        self.client = client
        self.config = config

    async def get_top_movers(self, limit: int = 10) -> List[Dict]:
        tickers = await self.client.fetch_tickers()
        sorted_tickers = sorted(
            tickers.values(),
            key=lambda x: abs(x['percentage']) if x['percentage'] is not None else 0,
            reverse=True
        )
        return [
            {
                'symbol': ticker['symbol'],
                'price_change_percent': ticker['percentage'],
                'current_price': ticker['last'],
                'volume': ticker['quoteVolume']
            }
            for ticker in sorted_tickers[:limit]
        ]

    async def get_market_summary(self) -> Dict:
        tickers = await self.client.fetch_tickers()
        total_volume = sum(ticker['quoteVolume'] for ticker in tickers.values() if ticker['quoteVolume'] is not None)
        return {
            'total_markets': len(tickers),
            'total_volume': total_volume,
            'top_gainers': await self.get_top_movers(limit=5),
            'top_losers': sorted(await self.get_top_movers(limit=100), key=lambda x: x['price_change_percent'])[:5]
        }

