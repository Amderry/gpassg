from fastapi import FastAPI, Depends
from routers import publickey, entry
from routers import challenge as challenge_router
from middleware import challenge
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
app.include_router(publickey.router, prefix="/publickey")
app.include_router(entry.router, prefix="/entry")
app.include_router(challenge_router.router, prefix="/challenge")
app.add_middleware(BaseHTTPMiddleware, dispatch=challenge.challenge_middleware)
