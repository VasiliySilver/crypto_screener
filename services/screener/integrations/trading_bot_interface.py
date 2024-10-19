import aiohttp

class TradingBotInterface:
    def __init__(self, bot_api_url):
        self.bot_api_url = bot_api_url

    async def send_signal(self, signal_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.bot_api_url}/signal", json=signal_data) as response:
                return await response.json()

