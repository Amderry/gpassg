from pydantic import BaseModel
from typing import Optional

class Challenge(BaseModel):
  fingerprint: str
  secret: str
