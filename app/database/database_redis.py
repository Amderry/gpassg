from .database_abstract import Database
import redis

class Redis(Database):
  def __init__(self, host: str, port: int, password: str = None, username: str = None):
    self.client = redis.Redis(host=host, port=port, password=password, username=username)

  def add_to_db(self, name: str, key: str, value: str):
    return self.client.hset(name, key, value)

  def delete_from_db(self, key):
    pass

  def edit_in_db(self, key: str, value: str):
    pass

  def get_from_db(self, name: str, key: str):
    return self.client.hget(name, key)
