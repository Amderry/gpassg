from fastapi import status, Body, APIRouter, Depends, Response
from schemas.publickey import PublicKey
from utils.gnupg import import_publickey, get_fingerprints 
from database.database_fabric import get_database

router = APIRouter()

@router.post("/import", status_code=200)
async def route_publickey_import(publickey: PublicKey, response: Response):
  import_result = import_publickey(publickey.key_text)
  if import_result.returncode != 0:
    response.status_code = status.HTTP_400_BAD_REQUEST
    return {"fingerprints": []}
  push_publickey(publickey.key_text, get_database())
  return {"fingerprints": import_result.results}

def push_publickey(publickey: str, database):
  fingerprints = get_fingerprints(publickey)
  for fp in fingerprints:
    database.add_to_db(fp, publickey)
