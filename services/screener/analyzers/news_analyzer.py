import aiohttp
from bs4 import BeautifulSoup
from ..config import Config

class NewsAnalyzer:
    def __init__(self, config: Config):
        self.config = config

    async def analyze_recent_news(self, symbol: str):
        url = f"https://cryptonews.com/news/tag/{symbol.lower()}/"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')
        news_items = soup.find_all('div', class_='cn-tile article')
        
        recent_news = []
        for item in news_items[:5]:  # Get the 5 most recent news
            title = item.find('h4', class_='cn-tile-title').text.strip()
            link = item.find('a', class_='cn-tile-title')['href']
            recent_news.append({'title': title, 'link': link})
        
        return {
            'symbol': symbol,
            'recent_news': recent_news
        }

