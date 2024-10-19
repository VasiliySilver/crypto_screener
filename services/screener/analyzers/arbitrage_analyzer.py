from ..exchange.multi_exchange_client import MultiExchangeClient

class ArbitrageAnalyzer:
    def __init__(self, client: MultiExchangeClient):
        self.client = client

    async def find_arbitrage_opportunities(self, symbol: str):
        opportunities = []
        tickers = {ex_id: await self.client.fetch_tickers(ex_id) for ex_id in self.client.exchanges}
        
        for ex1_id, ex1_tickers in tickers.items():
            for ex2_id, ex2_tickers in tickers.items():
                if ex1_id != ex2_id:
                    price1 = ex1_tickers[symbol]['last']
                    price2 = ex2_tickers[symbol]['last']
                    
                    if price1 and price2:
                        diff = (price2 - price1) / price1 * 100
                        if abs(diff) > 1:  # 1% threshold
                            opportunities.append({
                                'symbol': symbol,
                                'exchange1': ex1_id,
                                'exchange2': ex2_id,
                                'price1': price1,
                                'price2': price2,
                                'difference_percent': diff
                            })
        
        return opportunities

