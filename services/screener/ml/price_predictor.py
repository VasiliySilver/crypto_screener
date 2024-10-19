from sklearn.ensemble import RandomForestRegressor
import numpy as np
from ..exchange.client import ExchangeClient

class PricePredictor:
    def __init__(self, client: ExchangeClient):
        self.client = client
        self.model = RandomForestRegressor(n_estimators=100)

    async def train_and_predict(self, symbol: str, timeframe: str = '1h'):
        ohlcv = await self.client.fetch_ohlcv(symbol, timeframe, limit=1000)
        data = np.array([candle[1:] for candle in ohlcv])
        
        X = data[:-1]
        y = data[1:, 3]  # Predict close price
        
        self.model.fit(X, y)
        
        latest_data = data[-1].reshape(1, -1)
        prediction = self.model.predict(latest_data)[0]
        
        return {
            'symbol': symbol,
            'current_price': data[-1, 3],
            'predicted_price': prediction,
            'predicted_change': (prediction - data[-1, 3]) / data[-1, 3] * 100
        }

