from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi import FastAPI
import aioredis
import os

async def init_rate_limiter(app: FastAPI):
    redis = await aioredis.from_url(os.getenv("REDIS_URL"), encoding="utf8", decode_responses=True)
    await FastAPILimiter.init(redis)
    app.state.limiter = FastAPILimiter
