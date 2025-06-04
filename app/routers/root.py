from fastapi import status, Body, APIRouter, Depends, Response
from config import VERSION 

router = APIRouter()

@router.get("/", status_code=200)
async def root_get()
  return {"description": "Greetings! This app is a zero-knowledge password vault that uses OpenPGP standart to store and encrypt your messages. In general, it's not limited to store only passwords and sensitive data, every file that can be encrypted lies perfectly in this concept.", "version": VERSION} 
