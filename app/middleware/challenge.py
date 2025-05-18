from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from database.database_fabric import get_database
from json import loads

async def challenge_middleware(request: Request, call_next):
  if request.url.path not in ['/entry/post', '/entry/get']:
    return await call_next(request)
  else:
    if request.method == 'GET':
      fingerprint = request.query_params['fingerprint']
    else:
      fingerprint = loads(await request.body())['fingerprint']
    challenge_passed = get_database().get_from_db(f'{fingerprint}:challenge_passed')
    if challenge_passed == None or challenge_passed == b'false':
      return JSONResponse(content={"info": "challenge required"}, status_code=status.HTTP_401_UNAUTHORIZED)
    else:
      return await call_next(request)
