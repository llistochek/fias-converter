from abc import ABC, abstractmethod

Row = dict[str, str]


class BaseAdapter(ABC):

    @abstractmethod
    def __init__(self, url: str, **kwargs):
        pass

    @abstractmethod
    def create_table(self, name: str, columns: list[tuple[str, str]]):
        pass

    @abstractmethod
    def insert_row(self, table: str, data: Row):
        pass

    def upsert_row(self, table: str, data: Row):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass
