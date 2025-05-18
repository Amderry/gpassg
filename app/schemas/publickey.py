from pydantic import BaseModel

class PublicKey(BaseModel):
  fingerprint: str
  key_text: str
  challenge: str = None
