from fastapi import status, Body, APIRouter, Depends, Response
from schemas.entry import Entry
from database.database_fabric import get_database
from utils.gnupg import encrypt_message, get_recipients
from utils.sha256 import hash_str

router = APIRouter()

@router.post("/post", status_code=200)
async def route_entry_post(entry: Entry, response: Response):
  if entry.encrypted:
    recipients = get_recipients(entry.message)
    if len(recipients) == 0:
      response.status_code = status.HTTP_400_BAD_REQUEST
      recipients = "not a valid PGP message"
    else:
      get_database().add_to_db(f'fingerprint:{entry.fingerprint}:message:{hash_str(entry.key)}', entry.message)
    return {"result": recipients}
  else:
    encrypt_result = encrypt_message(entry.message, entry.fingerprint)
    if not encrypt_result.ok:
      response.status_code = status.HTTP_400_BAD_REQUEST
    else:
      sha256.update(entry.key.encode('utf-8'))
      hashed_key = sha256.hexdigest()
      get_database().add_to_db(f'fingerprint:{entry.fingerprint}:message:{hash_str(entry.key)}', encrypt_result.data)
    return {"result": encrypt_result.status}

@router.get("/get", status_code=200)
async def route_entry_get(fingerprint: str, key: str, response: Response):
  result = get_database().get_from_db(f'fingerprint:{fingerprint}:message:{hash_str(key)}')
  if result == None:
    response.status_code = status.HTTP_404_NOT_FOUND
  return {"result": result}

@router.delete("/delete", status_code=200)
async def route_entry_delete(fingerprint: str, key: str, response: Response):
  result = get_database().delete_from_db(f'fingerprint:{fingerprint}:message:{hash_str(key)}')
  if result == None:
    response.status_code = status.HTTP_404_NOT_FOUND
  return {"result": result}
