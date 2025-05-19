from fastapi import status, Body, APIRouter, Depends, Response
from database.database_fabric import get_database
from utils.gnupg import encrypt_message, import_publickey
from schemas.challenge import Challenge
import random
import string

router = APIRouter()

@router.post("/post")
async def route_challenge_post(challenge: Challenge, response: Response):
  challenge_result = check_challenge(challenge.fingerprint)
  print(challenge_result, flush=True)
  secret = get_database().get_from_db(f'{challenge.fingerprint}:challenge')

  if challenge_result == None:
    message = "no challenge, request one"
  elif not challenge_result:
    if secret.decode('utf-8') == challenge.secret:
      pass_challenge(challenge.fingerprint, 120)
      message = "challenge passed, you have 2 min to go"
    else:
      response.status_code = status.HTTP_401_UNAUTHORIZED
      message = "gtfo"
  elif challenge_result:
    message = "challenge already passed"
    
  return {"result": message}

@router.get("/get")
async def route_challenge_get(fingerprint: str, response: Response):
  key = get_database().get_from_db(f'{fingerprint}:publickey')
  if key == None:
    response.status_code = status.HTTP_404_NOT_FOUND
    message = "key not found"
  else:
    import_publickey(key)
    challenge_result = check_challenge(fingerprint)
    print(challenge_result, flush=True)
    if challenge_result == None:
      message = "You have 60 seconds before your challenge expires! Your challenge secret: " + create_challenge(fingerprint) + '\n'
      message = encrypt_message(message, fingerprint).data
    elif not challenge_result:
      message = "you already have pending challenge"
    else:
      message = ""

  return {"result": message}

def create_challenge(fingerprint: str):
  secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
  get_database().add_to_db(f'{fingerprint}:challenge', secret, 60)
  get_database().add_to_db(f'{fingerprint}:challenge_passed', 'false', 60)
  return secret

def check_challenge(fingerprint: str):
  challenge_result = get_database().get_from_db(f'{fingerprint}:challenge_passed')
  if challenge_result != None:
    return challenge_result.decode('utf-8') in ['true']
  else:
    return None

def pass_challenge(fingerprint: str, ttl: int):
  get_database().add_to_db(f'{fingerprint}:challenge_passed', 'true', ttl)
