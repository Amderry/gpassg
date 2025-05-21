from fastapi import status, Body, APIRouter, Depends, Response
from schemas.publickey import PublicKey
from utils.gnupg import import_publickey, get_fingerprints, delete_publickey, encrypt_message 
from database.database_fabric import get_database
from .challenge import check_challenge, create_challenge
import random
import string

router = APIRouter()

@router.post("/import", status_code=200)
async def route_publickey_import(publickey: PublicKey, response: Response):
  push_publickey(publickey.key_text)
  import_result = import_publickey_wrapper(publickey.key_text)
  return {"import": import_result}

def push_publickey(publickey: str):
  fingerprints = get_fingerprints_wrapper(publickey)
  for fp in fingerprints:
    get_database().add_to_db(f'fingerprint:{fp}:publickey', publickey)

def del_publickey(fingerprint: str):
  get_database().delete_from_db(f'fingerprint:{fingerprint}:publickey')

def get_publickey(fingerprint: str):
  return get_database().get_from_db(f'fingerprint:{fingerprint}:publickey')

def import_publickey_wrapper(key_text: str):
  push_publickey(key_text)
  return import_publickey(key_text).fingerprints[0]

def delete_publickey_wrapper(fingerprint: str):
  del_publickey(fingerprint)
  return delete_publickey(fingerprint)

def get_fingerprints_wrapper(key_text: str):
  return get_fingerprints(key_text)
