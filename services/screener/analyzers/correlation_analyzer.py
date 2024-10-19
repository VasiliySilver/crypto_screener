from typing import List, Dict
import pandas as pd
from ..exchange.client import ExchangeClient

class CorrelationAnalyzer:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def analyze_correlations(self, base_symbol: str, compare_symbols: List[str]) -> Dict:
        base_data = await self.get_asset_data(base_symbol, 100)
        base_prices = [candle['close'] for candle in base_data]
        
        correlations = {}
        for symbol in compare_symbols:
            compare_data = await self.get_asset_data(symbol, 100)
            compare_prices = [candle['close'] for candle in compare_data]
            
            df = pd.DataFrame({'base': base_prices, 'compare': compare_prices})
            correlation = df['base'].corr(df['compare'])
            correlations[symbol] = correlation
        
        return correlations

    async def get_asset_data(self, symbol: str, num_candles: int) -> List[Dict]:
        ohlcv = await self.client.fetch_ohlcv(symbol, '1h', None, num_candles)
        return [
            {
                'timestamp': candle[0],
                'open': candle[1],
                'high': candle[2],
                'low': candle[3],
                'close': candle[4],
                'volume': candle[5]
            }
            for candle in ohlcv
        ]

