from fastapi import FastAPI, Depends
from routers import publickey, entry

app = FastAPI()
app.include_router(publickey.router, prefix="/publickey")
app.include_router(entry.router, prefix="/entry")
