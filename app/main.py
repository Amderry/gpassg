from fastapi import FastAPI, Depends
from routers import publickey, entry, root
from routers import challenge as challenge_router
from middleware.challenge import ChallengeMiddleware

app = FastAPI()
app.include_router(root.router)
app.include_router(publickey.router, prefix="/publickey")
app.include_router(entry.router, prefix="/entry")
app.include_router(challenge_router.router, prefix="/challenge")
app.add_middleware(ChallengeMiddleware)
