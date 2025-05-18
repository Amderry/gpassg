from fastapi import status, Body, APIRouter, Depends, Response
from database.database_fabric import get_database
from utils.gnupg import encrypt_message, import_publickey
from schemas.challenge import Challenge
import random
import string

router = APIRouter()

@router.post("/post")
async def route_challenge_post(challenge: Challenge, response: Response):
  challenge_result = get_database().get_from_db(f'{challenge.fingerprint}:challenge_passed')
  if challenge_result == b'false':
    secret = get_database().get_from_db(f'{challenge.fingerprint}:challenge').decode('utf-8')
    if secret == challenge.secret:
      get_database().add_to_db(f'{challenge.fingerprint}:challenge_passed', 'true', 120)
      message = "challenge passed, you have 2 min to go"
    else:
      response.status_code = status.HTTP_401_UNAUTHORIZED
      message = "gtfo"
  elif challenge_result == b'true':
    message = "already passed"
  else:
    message = "no challenge, request one"
  return {"result": message}

@router.get("/get")
async def route_challenge_get(fingerprint: str, response: Response):
  key = get_database().get_from_db(f'{fingerprint}:publickey')
  if key == None:
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"result": "key not found"} 
  import_publickey(key)
  challenge_result = get_database().get_from_db(f'{fingerprint}:challenge_passed')
  print(challenge_result, flush=True)
  if challenge_result == None:
    secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
    get_database().add_to_db(f'{fingerprint}:challenge', secret, 60)
    get_database().add_to_db(f'{fingerprint}:challenge_passed', 'false', 60)
    encrypted_challenge = encrypt_message("You have 60 seconds before your challenge expires! Your challenge secret: " + secret + "\n", fingerprint)
  elif challenge_result == b'false':
    return {"result": "you already have pending challenge"}
  elif challenge_result == b'true':
    return {"result": "already passed challenge, wait for a bit"}
  return {"result": encrypted_challenge.data}
