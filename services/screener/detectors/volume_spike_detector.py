from typing import List, Dict
from ..exchange.client import ExchangeClient
from ..config import Config

class VolumeSpikeDetector:
    def __init__(self, client: ExchangeClient, config: Config):
        self.client = client
        self.config = config

    async def screen_volume_spikes(self) -> List[Dict]:
        tickers = await self.client.fetch_tickers()
        volume_spikes = []

        for symbol, ticker in tickers.items():
            if ticker['quoteVolume'] and ticker['previousClose']:
                volume_change = (ticker['quoteVolume'] - ticker['previousClose']) / ticker['previousClose'] * 100
                if volume_change > self.config.VOLUME_THRESHOLD_PERCENT:
                    volume_spikes.append({
                        'symbol': symbol,
                        'volume_change_percent': volume_change,
                        'current_volume': ticker['quoteVolume'],
                        'current_price': ticker['last']
                    })

        return sorted(volume_spikes, key=lambda x: x['volume_change_percent'], reverse=True)

