from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from json import loads
from urllib.parse import urlencode
from routers.publickey import import_publickey_wrapper, delete_publickey_wrapper, get_publickey, get_fingerprints_wrapper
from routers.challenge import check_challenge 
from pydantic import ValidationError

class ChallengeMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request, call_next):
    base_path = request.url.path

    # Check if incoming request to any of /entry routes have a pending challenge
    if base_path in ['/entry/get', '/entry/delete']:
      try:
        print(request.query_params['fingerprint'], flush=False)
        fingerprint = request.query_params['fingerprint']
      except:
        return JSONResponse(content={"error": "bad request"}, status_code=status.HTTP_400_BAD_REQUEST)
      challenge_creation_needed = challenge_exists(fingerprint)
      if challenge_creation_needed:
        return JSONResponse(content={"info": "challenge required"}, status_code=status.HTTP_401_UNAUTHORIZED)
      return await call_next(request)

    elif base_path in ['/entry/post']:
      body = await request.body()
      try:
        fingerprint = fingerprint = loads(body)['fingerprint']
      except:
        return JSONResponse(content={"error": "bad request"}, status_code=status.HTTP_400_BAD_REQUEST)
      challenge_creation_needed = challenge_exists(fingerprint)
      if challenge_creation_needed:
        return JSONResponse(content={"info": "challenge required"}, status_code=status.HTTP_401_UNAUTHORIZED)
      return await call_next(request)

    # Proceed incoming request to any of /publickey routes (it requires more complicated logic). Importing publickey and then instantly deleting it assuming that client have no access to his key apriori and if he returns right challenge - import it again, now permanently.
    elif base_path.startswith('/publickey'):
      body = await request.body()
      print(body, flush=False)
      try:
        fingerprint = get_fingerprints_wrapper(loads(body)['key_text'])[0]
      except:
        return JSONResponse(status_code=400, content={"error": "bad request"})
      challenge_result = check_challenge(fingerprint)
      publickey_exists = get_publickey(fingerprint)
      if (challenge_result == None or not challenge_result) and not publickey_exists:
        import_publickey_wrapper(loads(body)['key_text'])
        request.scope['path'] = request.url.path.replace("/publickey/import", f'/challenge/get')
        request.scope['method'] = 'GET'
        query_params = {"fingerprint": fingerprint}
        request.scope['query_string'] = urlencode(query_params).encode('utf-8')
      response = await call_next(request)
      if (challenge_result == None or not challenge_result) and not publickey_exists:
        delete_publickey_wrapper(fingerprint)
      return response
    else:
      return await call_next(request)

def challenge_exists(fingerprint: str):
  challenge_passed = check_challenge(fingerprint)
  return challenge_passed == None
