from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from routers.challenge import check_challenge 
from routers.publickey import import_publickey_wrapper, delete_publickey_wrapper, get_publickey, get_fingerprints_wrapper
from json import loads
from urllib.parse import urlencode

async def challenge_middleware(request: Request, call_next):
  if request.url.path == '/publickey/import':
    fingerprint = get_fingerprints_wrapper(loads(await request.body())['key_text'])[0]
    challenge_result = check_challenge(fingerprint)
    publickey_exists = get_publickey(fingerprint)
    if (challenge_result == None or not challenge_result) and not publickey_exists:
      import_publickey_wrapper(loads(await request.body())['key_text'])
      request.scope['path'] = request.url.path.replace("/publickey/import", f'/challenge/get')
      request.scope['method'] = 'GET'
      query_params = {"fingerprint": fingerprint}
      request.scope['query_string'] = urlencode(query_params).encode('utf-8')
    response = await call_next(request)
    if (challenge_result == None or not challenge_result) and not publickey_exists:
      delete_publickey_wrapper(fingerprint)
    return response
  elif request.url.path in ['/challenge/get', '/challenge/post']:
    return await call_next(request)
  else:
    if request.method == 'GET' or request.method == 'DELETE':
      fingerprint = request.query_params['fingerprint']
    else:
      fingerprint = loads(await request.body())['fingerprint']
    challenge_passed = check_challenge(fingerprint)
    if not challenge_passed:
      return JSONResponse(content={"info": "challenge required"}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
      return await call_next(request)
