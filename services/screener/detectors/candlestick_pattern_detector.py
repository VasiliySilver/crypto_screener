import talib
import numpy as np
from ..exchange.client import ExchangeClient

class CandlestickPatternDetector:
    def __init__(self, client: ExchangeClient):
        self.client = client
        self.patterns = {
            'DOJI': talib.CDLDOJI,
            'HAMMER': talib.CDLHAMMER,
            'ENGULFING': talib.CDLENGULFING,
            'MORNING_STAR': talib.CDLMORNINGSTAR,
            'EVENING_STAR': talib.CDLEVENINGSTAR
        }

    async def detect_patterns(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=100)
        open_prices = np.array([candle[1] for candle in ohlcv])
        high_prices = np.array([candle[2] for candle in ohlcv])
        low_prices = np.array([candle[3] for candle in ohlcv])
        close_prices = np.array([candle[4] for candle in ohlcv])
        
        detected_patterns = {}
        for pattern_name, pattern_func in self.patterns.items():
            result = pattern_func(open_prices, high_prices, low_prices, close_prices)
            if result[-1] != 0:
                detected_patterns[pattern_name] = 'Bullish' if result[-1] > 0 else 'Bearish'
        
        return {
            'symbol': symbol,
            'detected_patterns': detected_patterns
        }

