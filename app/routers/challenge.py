from fastapi import status, Body, APIRouter, Depends, Response
from database.database_fabric import get_database
from utils.gnupg import encrypt_message, import_publickey
from schemas.challenge import Challenge
import random
import string

router = APIRouter()

@router.post("/post")
async def route_challenge_post(challenge: Challenge, response: Response):
  comparison = compare_secret(challenge.fingerprint, challenge.secret)
  if comparison == None:
    message = "no challenge, request one"
  elif comparison:
    pass_challenge(challenge.fingerprint, 120)
    message = "challenge passed, you have 2 min to go"
  else:
    message = "gtfo"
    response.status_code = status.HTTP_401_UNAUTHORIZED
  return {"result": message}

@router.get("/get")
async def route_challenge_get(fingerprint: str, response: Response):
  key = get_database().get_from_db(f'fingerprint:{fingerprint}:publickey')
  if key == None:
    response.status_code = status.HTTP_404_NOT_FOUND
    message = "key not found"
  else:
    import_publickey(key)
    challenge_result = check_challenge(fingerprint)
    print(challenge_result, flush=True)
    if challenge_result == None:
      message = create_challenge(fingerprint)
    elif not challenge_result:
      message = "you already have pending challenge"
    else:
      message = ""

  return {"result": message}

def create_challenge(fingerprint: str):
  message = "You have 60 seconds before your challenge expires! Your challenge secret: "
  secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
  get_database().add_to_db(f'fingerprint:{fingerprint}:challenge', secret, 60)
  get_database().add_to_db(f'fingerprint:{fingerprint}:challenge_passed', 'false', 60)
  return encrypt_message(secret + '\n', fingerprint).data

def check_challenge(fingerprint: str):
  challenge_result = get_database().get_from_db(f'fingerprint:{fingerprint}:challenge_passed')
  if challenge_result != None:
    return challenge_result.decode('utf-8') in ['true']
  else:
    return None

def pass_challenge(fingerprint: str, ttl: int):
  get_database().add_to_db(f'fingerprint:{fingerprint}:challenge_passed', 'true', ttl)

def compare_secret(fingerprint: str, secret: str):
  challenge_result = check_challenge(fingerprint)
  if challenge_result == None:
    return None
  elif challenge_result:
    return True
  else:
    db_secret = get_database().get_from_db(f'fingerprint:{fingerprint}:challenge').decode('utf-8')
    return db_secret == secret
