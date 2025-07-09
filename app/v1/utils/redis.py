import redis.asyncio as Redis
from app.v1.utils.settings import Config

JTI_EXPIRY = 3600

redis_url = f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/0"
token_blocklist = Redis.from_url(redis_url, decode_responses=True)

async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(
        name=jti,
        value="",
        ex=JTI_EXPIRY
    )

async def token_in_blocklist(jti: str) -> bool:
    try:
        result = await token_blocklist.get(name=jti)
        return result is not None
    except Exception as e:
        print(f">>>Redis connection failed: {e}")
        return False