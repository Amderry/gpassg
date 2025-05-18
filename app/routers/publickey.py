from fastapi import status, Body, APIRouter, Depends, Response
from schemas.publickey import PublicKey
from utils.gnupg import import_publickey, get_fingerprints, delete_key, encrypt_message 
from database.database_fabric import get_database
import random
import string

router = APIRouter()

@router.post("/import", status_code=200)
async def route_publickey_import(publickey: PublicKey, response: Response):
  database_key = get_database().get_from_db(f'{publickey.fingerprint}:publickey')
  challenge_pending = get_database().get_from_db(f'{publickey.fingerprint}:import_challenge_passed')
  if database_key == None and challenge_pending == None:
    import_result = import_publickey(publickey.key_text)
    if import_result.returncode != 0:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return {"fingerprints": []}
    secret = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(32))
    get_database().add_to_db(f'{publickey.fingerprint}:import_challenge', secret, 60)
    get_database().add_to_db(f'{publickey.fingerprint}:import_challenge_passed', 'false', 60)
    encrypted_challenge = encrypt_message("You have 60 seconds before your challenge expires! Your challenge secret: " + secret + "\n", publickey.fingerprint).data
    delete_key(publickey.fingerprint)
    return {"challenge": encrypted_challenge}
  elif challenge_pending != None:
    secret = get_database().get_from_db(f'{publickey.fingerprint}:import_challenge')
    challenge_passed = get_database().get_from_db(f'{publickey.fingerprint}:import_challenge_passed')
    if challenge_passed == b'false':
      if secret.decode('utf-8') ==  publickey.challenge:
        push_publickey(publickey.key_text, get_database())
        import_result = import_publickey(publickey.key_text)
        return {"fingerprints": import_result.fingerprints}
      else:
        return {"challenge": "gtfo"}
  else:
    return {"fingerprints": f"already imported {publickey.fingerprint}"}

def push_publickey(publickey: str, database):
  fingerprints = get_fingerprints(publickey)
  for fp in fingerprints:
    database.add_to_db(f'{fp}:publickey', publickey)
