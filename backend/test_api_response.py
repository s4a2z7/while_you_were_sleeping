import asyncio
import json
from api.stocks import get_trending_stocks

async def test():
    result = await get_trending_stocks("most_actives")
    print(json.dumps(result, indent=2, default=str))

asyncio.run(test())
