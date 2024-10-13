import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import Column, Double, Integer, String, Table, create_engine
from sqlalchemy.types import TypeEngine

from .base import BaseAdapter, Row

_TYPE_MAPPINGS = {
    "xs:string": String,
    "xs:decimal": Double,
    "xs:date": String,
    "xs:boolean": Integer,
    "xs:anySimpleType": String,
    "xs:long": Integer,
    "xs:integer": Integer,
    "xs:int": Integer,
    "xs:byte": Integer,
}


class SqlalchemyAdapter(BaseAdapter):
    __engine: sqlalchemy.Engine
    __meta: sqlalchemy.MetaData
    __connection: sqlalchemy.Connection

    def __init__(self, url: str, **kwargs):
        self.__engine = create_engine(url, **kwargs)
        self.__meta = sqlalchemy.MetaData()
        self.__connection = self.__engine.connect()
        self.__meta.reflect(self.__engine)

    def __convert_type(self, raw_type: str) -> TypeEngine:
        return _TYPE_MAPPINGS.get(raw_type, String)

    def create_table(self, name: str, columns: list[tuple[str, str]]):
        if name not in self.__meta.tables:
            sql_columns = [
                Column(n, self.__convert_type(t), primary_key=(n == "ID"))
                for n, t in columns
            ]
            Table(name, self.__meta, *sql_columns)
            self.__meta.create_all(self.__connection)

    def insert_row(self, table: str, row: Row):
        alchemy_table = self.__meta.tables[table]
        self.__connection.execute(alchemy_table.insert(), row)

    def upsert_row(self, table: str, row: Row):
        alchemy_table = self.__meta.tables[table]
        try:
            self.__connection.execute(alchemy_table.insert(), row)
        except:
            stmt = alchemy_table.update().where(alchemy_table.c.ID == row["ID"])
            self.__connection.execute(stmt, row)

    def commit(self):
        self.__connection.commit()

    def close(self):
        self.commit()
        self.__connection.close()


fias_converter_adapter = SqlalchemyAdapter
