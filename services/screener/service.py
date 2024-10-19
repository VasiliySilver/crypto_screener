import asyncio
from typing import List, Dict
from .config import Config
from .exchange.client import ExchangeClient
from .analyzers.market_analyzer import MarketAnalyzer
from .analyzers.sentiment_analyzer import SentimentAnalyzer
from .analyzers.correlation_analyzer import CorrelationAnalyzer
from .detectors.pump_dump_detector import PumpDumpDetector
from .detectors.volatility_detector import VolatilityDetector
from .detectors.volume_spike_detector import VolumeSpikeDetector
from .analyzers.technical_analyzer import TechnicalAnalyzer
from .analyzers.volume_analyzer import VolumeAnalyzer
from .analyzers.news_analyzer import NewsAnalyzer
from .detectors.divergence_detector import DivergenceDetector
from .detectors.support_resistance_detector import SupportResistanceDetector
from .analyzers.orderbook_analyzer import OrderbookAnalyzer
from .detectors.candlestick_pattern_detector import CandlestickPatternDetector
from .analyzers.social_sentiment_analyzer import SocialSentimentAnalyzer
from .detectors.anomaly_detector import AnomalyDetector
from .analyzers.liquidity_analyzer import LiquidityAnalyzer
from .ml.price_predictor import PricePredictor
from .exchange.multi_exchange_client import MultiExchangeClient
from .analyzers.arbitrage_analyzer import ArbitrageAnalyzer
from .notifiers.real_time_notifier import RealTimeNotifier
from .integrations.trading_bot_interface import TradingBotInterface
from .analyzers.advanced_sentiment_analyzer import AdvancedSentimentAnalyzer
from .analyzers.blockchain_analyzer import BlockchainAnalyzer
from .analyzers.regulatory_risk_analyzer import RegulatoryRiskAnalyzer
from .detectors.insider_trading_detector import InsiderTradingDetector
from .analyzers.macro_economic_analyzer import MacroEconomicAnalyzer
from .analyzers.ecosystem_analyzer import EcosystemAnalyzer
from .analyzers.tokenomics_analyzer import TokenomicsAnalyzer

class ScreenerService:
    def __init__(self, config: Config):
        self.config = config
        self.client = ExchangeClient(config)
        self.market_analyzer = MarketAnalyzer(self.client, config)
        self.sentiment_analyzer = SentimentAnalyzer()
        self.correlation_analyzer = CorrelationAnalyzer(self.client)
        self.pump_dump_detector = PumpDumpDetector(self.client, config)
        self.volatility_detector = VolatilityDetector(self.client, config)
        self.volume_spike_detector = VolumeSpikeDetector(self.client, config)
        self.technical_analyzer = TechnicalAnalyzer(self.client)
        self.volume_analyzer = VolumeAnalyzer(self.client)
        self.news_analyzer = NewsAnalyzer(config)
        self.divergence_detector = DivergenceDetector(self.client)
        self.support_resistance_detector = SupportResistanceDetector(self.client)
        self.orderbook_analyzer = OrderbookAnalyzer(self.client)
        self.candlestick_pattern_detector = CandlestickPatternDetector(self.client)
        self.social_sentiment_analyzer = SocialSentimentAnalyzer(config)
        self.anomaly_detector = AnomalyDetector(self.client)
        self.liquidity_analyzer = LiquidityAnalyzer(self.client)
        self.multi_exchange_client = MultiExchangeClient(config.EXCHANGE_IDS)
        self.price_predictor = PricePredictor(self.multi_exchange_client)
        self.arbitrage_analyzer = ArbitrageAnalyzer(self.multi_exchange_client)
        self.real_time_notifier = RealTimeNotifier()
        self.trading_bot_interface = TradingBotInterface(config.BOT_API_URL)
        self.advanced_sentiment_analyzer = AdvancedSentimentAnalyzer()
        self.blockchain_analyzer = BlockchainAnalyzer(config)
        self.regulatory_risk_analyzer = RegulatoryRiskAnalyzer(config)
        self.insider_trading_detector = InsiderTradingDetector(self.client)
        self.macro_economic_analyzer = MacroEconomicAnalyzer(config)
        self.ecosystem_analyzer = EcosystemAnalyzer(config)
        self.tokenomics_analyzer = TokenomicsAnalyzer(self.client)

    async def get_top_movers(self, limit: int = 10):
        return await self.market_analyzer.get_top_movers(limit)

    async def get_market_summary(self):
        return await self.market_analyzer.get_market_summary()

    async def analyze_market_sentiment(self, symbol: str):
        return await self.sentiment_analyzer.analyze_market_sentiment(symbol)

    async def analyze_correlations(self, base_symbol: str, compare_symbols: list):
        return await self.correlation_analyzer.analyze_correlations(base_symbol, compare_symbols)

    async def detect_pump_and_dump(self):
        return await self.pump_dump_detector.detect_pump_and_dump()

    async def screen_volatility(self):
        return await self.volatility_detector.screen_volatility()

    async def screen_volume_spikes(self):
        return await self.volume_spike_detector.screen_volume_spikes()

    async def close(self):
        await self.client.close()

    async def analyze_technical_indicators(self, symbol: str, timeframe: str = '1h'):
        return await self.technical_analyzer.analyze_technical_indicators(symbol, timeframe)

    async def analyze_volume_trends(self, symbol: str, timeframe: str = '1h'):
        return await self.volume_analyzer.analyze_volume_trends(symbol, timeframe)

    async def analyze_recent_news(self, symbol: str):
        return await self.news_analyzer.analyze_recent_news(symbol)

    async def detect_rsi_divergence(self, symbol: str, timeframe: str = '1h'):
        return await self.divergence_detector.detect_rsi_divergence(symbol, timeframe)

    async def detect_support_resistance(self, symbol: str, timeframe: str = '1h'):
        return await self.support_resistance_detector.detect_support_resistance(symbol, timeframe)

    async def analyze_orderbook(self, symbol: str, depth: int = 20):
        return await self.orderbook_analyzer.analyze_orderbook(symbol, depth)

    async def detect_candlestick_patterns(self, symbol: str, timeframe: str = '1h'):
        return await self.candlestick_pattern_detector.detect_patterns(symbol, timeframe)

    async def analyze_social_sentiment(self, symbol: str):
        return await self.social_sentiment_analyzer.analyze_social_sentiment(symbol)

    async def detect_anomalies(self, symbol: str, timeframe: str = '1h'):
        return await self.anomaly_detector.detect_anomalies(symbol, timeframe)

    async def analyze_liquidity(self, symbol: str):
        return await self.liquidity_analyzer.analyze_liquidity(symbol)

    async def predict_price(self, symbol: str, timeframe: str = '1h'):
        return await self.price_predictor.train_and_predict(symbol, timeframe)

    async def find_arbitrage_opportunities(self, symbol: str):
        return await self.arbitrage_analyzer.find_arbitrage_opportunities(symbol)

    async def send_real_time_notification(self, message):
        await self.real_time_notifier.broadcast(message)

    async def send_signal_to_bot(self, signal_data):
        return await self.trading_bot_interface.send_signal(signal_data)

    async def analyze_advanced_sentiment(self, symbol: str):
        return await self.advanced_sentiment_analyzer.analyze_sentiment(symbol)

    async def analyze_network_activity(self, symbol: str):
        return await self.blockchain_analyzer.analyze_network_activity(symbol)

    async def analyze_regulatory_risks(self, symbol: str):
        return await self.regulatory_risk_analyzer.analyze_regulatory_risks(symbol)

    async def detect_potential_insider_trading(self, symbol: str):
        return await self.insider_trading_detector.detect_potential_insider_trading(symbol)

    async def analyze_macro_impact(self, symbol: str):
        return await self.macro_economic_analyzer.analyze_macro_impact(symbol)

    async def analyze_ecosystem(self, symbol: str):
        return await self.ecosystem_analyzer.analyze_ecosystem(symbol)

    async def analyze_tokenomics(self, symbol: str):
        return await self.tokenomics_analyzer.analyze_tokenomics(symbol)
