from abc import ABC, abstractmethod

class Database(ABC):
  @abstractmethod
  def add_to_db(self, key: str, value: str):
    pass

  @abstractmethod
  def edit_in_db(self, key: str, value: str):
    pass

  @abstractmethod
  def delete_from_db(self, key: str):
    pass

  @abstractmethod
  def get_from_db(self, key: str):
    pass
