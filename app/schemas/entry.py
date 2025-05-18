from pydantic import BaseModel
from typing import Optional

class Entry(BaseModel):
  fingerprint: str
  key: str
  message: str
  encrypted: bool = True
