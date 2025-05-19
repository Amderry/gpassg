from pydantic import BaseModel

class PublicKey(BaseModel):
  key_text: str
