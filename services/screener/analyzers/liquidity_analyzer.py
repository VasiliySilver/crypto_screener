from ..exchange.client import ExchangeClient

class LiquidityAnalyzer:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def analyze_liquidity(self, symbol: str):
        ticker = await self.client.fetch_ticker(symbol)
        orderbook = await self.client.fetch_order_book(symbol)
        
        bid_ask_spread = (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['bids'][0][0]
        depth_1_percent = self._calculate_depth(orderbook, 0.01)
        depth_5_percent = self._calculate_depth(orderbook, 0.05)
        
        return {
            'symbol': symbol,
            'bid_ask_spread': bid_ask_spread,
            'depth_1_percent': depth_1_percent,
            'depth_5_percent': depth_5_percent,
            '24h_volume': ticker['quoteVolume']
        }

    def _calculate_depth(self, orderbook, percent):
        mid_price = (orderbook['asks'][0][0] + orderbook['bids'][0][0]) / 2
        lower_bound = mid_price * (1 - percent)
        upper_bound = mid_price * (1 + percent)
        
        buy_depth = sum(bid[1] for bid in orderbook['bids'] if bid[0] >= lower_bound)
        sell_depth = sum(ask[1] for ask in orderbook['asks'] if ask[0] <= upper_bound)
        
        return (buy_depth + sell_depth) / 2

