from fastapi import FastAPI
from routers import publickey

app = FastAPI()
app.include_router(publickey.router, prefix="/publickey")
