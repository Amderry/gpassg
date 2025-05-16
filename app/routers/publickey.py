from fastapi import status, Body 
from fastapi import APIRouter
from schemas.publickey import PublicKey

router = APIRouter()

@router.post("/add_publickey")
async def add_publickey(publickey: PublicKey):
  return {"echo": publickey}
