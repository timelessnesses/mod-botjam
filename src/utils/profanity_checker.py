import aiohttp


async def is_profane(setence):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "https://www.purgomalum.com/service/containsprofanity?text=" + setence
        ) as resp:
            if await resp.text() == "true":
                return True
            else:
                return False
