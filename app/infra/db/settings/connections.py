import os
from sqlalchemy import create_engine

class DBConnectionHandler:
    db_schema: str = os.getenv('DB_SCHEMA')
    db_server: str = os.getenv('DB_SERVER')
    db_port: str = os.getenv('DB_PORT')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_name: str = os.getenv('DB_NAME')

    def __init__(self) -> None:
        credentials = ""
        if self.db_user is not None:
            credentials = "{}:{}@".format(self.db_user, self.db_password)

        if self.db_schema is None:
            self.db_schema = "sqlite"

        if self.db_server is None:
            self.db_server = ""

        if self.db_name is None:
            self.db_name = ":memory:"

        db_port = ""
        if self.db_port is not None:
            db_port = ":{}".format(self.db_port)

        self.__connection_string = "{}://{}{}{}/{}".format(
            self.db_schema,
            credentials,
            self.db_server,
            db_port,
            self.db_name,
        )
        self._engine = self.__create_database_engine()

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self._engine
