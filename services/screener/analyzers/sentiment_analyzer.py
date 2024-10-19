from typing import List, Dict
import requests
from textblob import TextBlob

class SentimentAnalyzer:
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
        url = f"https://min-api.cryptocompare.com/data/v2/news/?categories={symbol}&excludeCategories=Sponsored"
        response = requests.get(url)
        return response.json()['Data']

    def analyze_sentiment(self, text: str) -> float:
        return TextBlob(text).sentiment.polarity

