import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBConnectionHandler:
    db_schema: str = os.getenv('DB_SCHEMA')
    db_server: str = os.getenv('DB_SERVER')
    db_port: str = os.getenv('DB_PORT')
    db_user: str = os.getenv('DB_USER')
    db_password: str = os.getenv('DB_PASSWORD')
    db_name: str = os.getenv('DB_NAME')
    scoped: bool = False

    def __enter__(self):
        make_session = sessionmaker(bind=self._engine) if not self.scoped else scoped_session(
            sessionmaker(bind=self._engine))
        self.session = make_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def __init__(self, scoped=False) -> None:
        print("instanciando ----")
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
        self.scoped = scoped
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_engine(self):
        return self._engine
