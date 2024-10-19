from typing import List, Dict
from ..exchange.client import ExchangeClient
from ..config import Config
import datetime

class PumpDumpDetector:
    def __init__(self, client: ExchangeClient, config: Config):
        self.client = client
        self.config = config

    async def detect_pump_and_dump(self) -> List[Dict]:
        top_movers = await self.get_top_movers(100)
        potential_pump_and_dump = []

        for asset in top_movers:
            if asset['price_change_percent'] > self.config.PRICE_THRESHOLD:
                asset_data = await self.get_asset_data(asset['symbol'], self.config.NUM_CANDLES)
                
                if self.is_pump_and_dump(asset_data):
                    potential_pump_and_dump.append({
                        'symbol': asset['symbol'],
                        'price_change_percent': asset['price_change_percent'],
                        'current_price': asset['current_price'],
                        'volume': asset['volume'],
                        'detected_at': datetime.datetime.now().isoformat()
                    })

        return potential_pump_and_dump

    def is_pump_and_dump(self, asset_data: List[Dict]) -> bool:
        if len(asset_data) < 2:
            return False

        price_changes = [
            (candle['close'] - candle['open']) / candle['open'] * 100
            for candle in asset_data
        ]

        max_increase = max(price_changes)
        if max_increase > self.config.PRICE_THRESHOLD:
            max_index = price_changes.index(max_increase)
            if max_index < len(price_changes) - 1:
                subsequent_change = price_changes[max_index + 1]
                if subsequent_change < 0 and abs(subsequent_change) > self.config.PRICE_THRESHOLD / 2:
                    return True

        return False

