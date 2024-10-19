import numpy as np
from ..exchange.client import ExchangeClient
import talib

class DivergenceDetector:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def detect_rsi_divergence(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=100)
        close_prices = np.array([candle[4] for candle in ohlcv])
        
        rsi = talib.RSI(close_prices)
        
        price_highs = np.argmax(close_prices[-30:])
        price_lows = np.argmin(close_prices[-30:])
        rsi_highs = np.argmax(rsi[-30:])
        rsi_lows = np.argmin(rsi[-30:])
        
        bullish_divergence = price_lows > rsi_lows
        bearish_divergence = price_highs < rsi_highs
        
        return {
            'symbol': symbol,
            'bullish_divergence': bullish_divergence,
            'bearish_divergence': bearish_divergence
        }

