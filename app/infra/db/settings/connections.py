import os
from sqlalchemy import create_engine
from pydantic_settings import SettingsConfigDict
from pydantic import (computed_field)


class DBConnectionHandler:
    DB_SCHEMA: str = os.getenv('DB_SCHEMA')
    DB_SERVER: str = os.getenv('DB_SERVER')
    DB_PORT: str = os.getenv('DB_PORT')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_NAME: str = os.getenv('DB_NAME')

    def __init__(self) -> None:
        credentials = ""
        if self.DB_USER is not None:
            credentials = "{}:{}@".format(self.DB_USER, self.DB_PASSWORD)
            
        if self.DB_SCHEMA is None:
            self.DB_SCHEMA = "sqlite"
            
        if self.DB_SERVER is None:
            self.DB_SERVER = ""
        
        if self.DB_NAME is None:
            self.DB_NAME = ":memory:"

        db_port = ""
        if self.DB_PORT is not None:
            db_port = ":{}".format(self.DB_PORT)

        self.__connection_string = "{}://{}{}{}/{}".format(
            self.DB_SCHEMA,
            credentials,
            self.DB_SERVER,
            db_port,
            self.DB_NAME,
        )
        self._engine = self.__create_database_engine()

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self._engine
