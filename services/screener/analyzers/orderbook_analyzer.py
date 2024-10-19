from ..exchange.client import ExchangeClient

class OrderbookAnalyzer:
    def __init__(self, client: ExchangeClient):
        self.client = client

    async def analyze_orderbook(self, symbol: str, depth: int = 20):
        orderbook = await self.client.fetch_order_book(symbol, depth)
        
        bid_ask_spread = (orderbook['asks'][0][0] - orderbook['bids'][0][0]) / orderbook['bids'][0][0]
        buy_wall = sum(bid[1] for bid in orderbook['bids'][:5])
        sell_wall = sum(ask[1] for ask in orderbook['asks'][:5])
        
        return {
            'symbol': symbol,
            'bid_ask_spread': bid_ask_spread,
            'buy_wall': buy_wall,
            'sell_wall': sell_wall,
            'buy_sell_ratio': buy_wall / sell_wall if sell_wall > 0 else float('inf')
        }

