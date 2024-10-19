import numpy as np
from scipy import stats
from ..exchange.client import ExchangeClient

class AnomalyDetector:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def detect_anomalies(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=100)
        close_prices = np.array([candle[4] for candle in ohlcv])
        volumes = np.array([candle[5] for candle in ohlcv])
        
        price_zscore = stats.zscore(close_prices)
        volume_zscore = stats.zscore(volumes)
        
        price_anomaly = abs(price_zscore[-1]) > 3
        volume_anomaly = abs(volume_zscore[-1]) > 3
        
        return {
            'symbol': symbol,
            'price_anomaly': price_anomaly,
            'volume_anomaly': volume_anomaly,
            'price_zscore': price_zscore[-1],
            'volume_zscore': volume_zscore[-1]
        }

