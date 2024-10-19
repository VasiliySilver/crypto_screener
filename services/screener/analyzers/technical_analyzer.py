import talib
import numpy as np
from ..exchange.client import ExchangeClient

class TechnicalAnalyzer:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def analyze_technical_indicators(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=100)
        close_prices = np.array([candle[4] for candle in ohlcv])
        
        rsi = talib.RSI(close_prices)
        macd, signal, _ = talib.MACD(close_prices)
        upper, middle, lower = talib.BBANDS(close_prices)
        
        return {
            'symbol': symbol,
            'rsi': rsi[-1],
            'macd': macd[-1],
            'macd_signal': signal[-1],
            'bollinger_upper': upper[-1],
            'bollinger_middle': middle[-1],
            'bollinger_lower': lower[-1]
        }

