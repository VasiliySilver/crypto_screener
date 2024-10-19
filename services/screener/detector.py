from typing import List, Dict
import ccxt.async_support as ccxt
import asyncio
from datetime import datetime, timedelta
from .config import Config
import talib
import numpy as np
from textblob import TextBlob
import requests
import pandas as pd

class CryptoMarketScreener:
    def __init__(self, config: Config):
        self.config = config
        self.exchange = getattr(ccxt, config.EXCHANGE_ID)()

    async def get_top_movers(self, limit: int = 10) -> List[Dict]:
        try:
            tickers = await self.exchange.fetch_tickers()
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
        except ccxt.NetworkError as e:
            raise Exception(f"Network error when fetching top movers: {str(e)}")
        except ccxt.ExchangeError as e:
            raise Exception(f"Exchange error when fetching top movers: {str(e)}")

    async def get_market_summary(self) -> Dict:
        try:
            tickers = await self.exchange.fetch_tickers()
            total_volume = sum(ticker['quoteVolume'] for ticker in tickers.values() if ticker['quoteVolume'] is not None)
            return {
                'total_markets': len(tickers),
                'total_volume': total_volume,
                'top_gainers': await self.get_top_movers(limit=5),
                'top_losers': sorted(await self.get_top_movers(limit=100), key=lambda x: x['price_change_percent'])[:5]
            }
        except ccxt.NetworkError as e:
            raise Exception(f"Network error when fetching market summary: {str(e)}")
        except ccxt.ExchangeError as e:
            raise Exception(f"Exchange error when fetching market summary: {str(e)}")

    async def detect_pump_and_dump(self) -> List[Dict]:
        top_movers = await self.get_top_movers(limit=100)
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
                        'detected_at': datetime.now().isoformat()
                    })

        return potential_pump_and_dump

    async def get_asset_data(self, symbol: str, num_candles: int) -> List[Dict]:
        try:
            since = int((datetime.now() - timedelta(hours=num_candles)).timestamp() * 1000)
            ohlcv = await self.exchange.fetch_ohlcv(symbol, self.config.TIMEFRAME, since, num_candles)
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
        except ccxt.NetworkError as e:
            raise Exception(f"Network error when fetching asset data: {str(e)}")
        except ccxt.ExchangeError as e:
            raise Exception(f"Exchange error when fetching asset data: {str(e)}")

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

    async def screen_liquidations(self) -> List[Dict]:
        try:
            # Примечание: не все биржи предоставляют данные о ликвидациях через API
            # Этот метод может потребовать дополнительной реализации или использования
            # специализированных API для получения данных о ликвидациях
            liquidations = await self.exchange.fetch_liquidations()
            return [
                liquidation for liquidation in liquidations
                if liquidation['amount'] > self.config.LIQUIDATION_THRESHOLD
            ]
        except ccxt.NetworkError as e:
            raise Exception(f"Network error when fetching liquidations: {str(e)}")
        except ccxt.ExchangeError as e:
            raise Exception(f"Exchange error when fetching liquidations: {str(e)}")

    async def screen_volatility(self) -> List[Dict]:
        tickers = await self.exchange.fetch_tickers()
        high_volatility_assets = []

        for symbol, ticker in tickers.items():
            if ticker['high'] and ticker['low']:
                volatility = (ticker['high'] - ticker['low']) / ticker['low']
                if volatility > self.config.VOLATILITY_THRESHOLD:
                    high_volatility_assets.append({
                        'symbol': symbol,
                        'volatility': volatility,
                        'current_price': ticker['last'],
                        'volume': ticker['quoteVolume']
                    })

        return sorted(high_volatility_assets, key=lambda x: x['volatility'], reverse=True)

    async def screen_funding_rates(self) -> List[Dict]:
        try:
            funding_rates = await self.exchange.fetch_funding_rates()
            high_funding_rates = [
                {'symbol': symbol, 'rate': rate['fundingRate']}
                for symbol, rate in funding_rates.items()
                if abs(rate['fundingRate']) > self.config.FUNDING_RATE_THRESHOLD
            ]
            return sorted(high_funding_rates, key=lambda x: abs(x['rate']), reverse=True)
        except ccxt.NetworkError as e:
            raise Exception(f"Network error when fetching funding rates: {str(e)}")
        except ccxt.ExchangeError as e:
            raise Exception(f"Exchange error when fetching funding rates: {str(e)}")

    async def screen_volume_spikes(self) -> List[Dict]:
        tickers = await self.exchange.fetch_tickers()
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

    async def close(self):
        await self.exchange.close()

    async def analyze_market_sentiment(self, symbol: str) -> Dict:
        news = await self.fetch_crypto_news(symbol)
        sentiment_scores = [self.analyze_sentiment(article['title']) for article in news]
        
        return {
            'average_sentiment': sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
            'sentiment_distribution': {
                'positive': sum(1 for score in sentiment_scores if score > 0.1),
                'neutral': sum(1 for score in sentiment_scores if -0.1 <= score <= 0.1),
                'negative': sum(1 for score in sentiment_scores if score < -0.1)
            }
        }

    async def fetch_crypto_news(self, symbol: str) -> List[Dict]:
        # Здесь нужно использовать API новостного сервиса, например, CryptoCompare
        url = f"https://min-api.cryptocompare.com/data/v2/news/?categories={symbol}&excludeCategories=Sponsored"
        response = requests.get(url)
        return response.json()['Data']

    def analyze_sentiment(self, text: str) -> float:
        return TextBlob(text).sentiment.polarity

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
