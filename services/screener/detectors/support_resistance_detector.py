import numpy as np
from ..exchange.client import ExchangeClient

class SupportResistanceDetector:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def detect_support_resistance(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=200)
        close_prices = np.array([candle[4] for candle in ohlcv])
        
        resistance_levels = self._find_levels(close_prices, is_resistance=True)
        support_levels = self._find_levels(close_prices, is_resistance=False)
        
        return {
            'symbol': symbol,
            'resistance_levels': resistance_levels,
            'support_levels': support_levels
        }

    def _find_levels(self, prices, is_resistance=True):
        levels = []
        for i in range(1, len(prices) - 1):
            if (is_resistance and prices[i] > prices[i-1] and prices[i] > prices[i+1]) or \
               (not is_resistance and prices[i] < prices[i-1] and prices[i] < prices[i+1]):
                levels.append(prices[i])
        return levels

