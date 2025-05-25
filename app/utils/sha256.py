import hashlib
import config

def hash_str(key: str):
  sha256 = hashlib.sha256()
  key = key.encode('utf-8')
  sha256.update(key)
  sha256.update(config.SALT)
  return sha256.hexdigest()
