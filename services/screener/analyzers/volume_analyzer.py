import numpy as np
from ..exchange.client import ExchangeClient

class VolumeAnalyzer:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def analyze_volume_trends(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=100)
        volumes = np.array([candle[5] for candle in ohlcv])
        
        avg_volume = np.mean(volumes)
        volume_trend = np.polyfit(range(len(volumes)), volumes, 1)[0]
        
        return {
            'symbol': symbol,
            'average_volume': avg_volume,
            'volume_trend': volume_trend,
            'current_volume': volumes[-1],
            'volume_change': (volumes[-1] - avg_volume) / avg_volume * 100
        }

