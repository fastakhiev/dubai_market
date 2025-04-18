import aiohttp

session: aiohttp.ClientSession | None = None

async def get_http_session() -> aiohttp.ClientSession:
    global session
    if not session:
        session = aiohttp.ClientSession()
    return session

async def close_http_session():
    global session
    if session:
        await session.close()
        session = None
