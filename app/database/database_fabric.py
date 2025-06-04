from .database_redis import Redis
import config

def get_database():
  if config.STORAGE_TYPE == None:
    raise Exception("Storage type is not set")
  elif config.STORAGE_TYPE.lower() == 'redis':
    return Redis(config.STORAGE_HOST, config.STORAGE_PORT, config.STORAGE_PASSWORD, config.STORAGE_USERNAME)
