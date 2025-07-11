import os
from pydantic import (
    PostgresDsn,
    computed_field,
    EmailStr
)
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    if "PYTEST_VERSION" not in os.environ:
        model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True,
                                          extra="ignore",)
        APP_NAME: str = ""
        POSTGRES_SERVER: str
        POSTGRES_PORT: int = 5432
        POSTGRES_USER: str
        POSTGRES_PASSWORD: str = ""
        POSTGRES_DB: str = ""

        FIRST_SUPERUSER: EmailStr
        FIRST_SUPERUSER_PASSWORD: str

        @computed_field  # type: ignore[prop-decorator]
        @property
        def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
            return MultiHostUrl.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )

        @computed_field
        @property
        def scoped_engine(self) -> bool: return False
    else:
        @computed_field  # type: ignore[prop-decorator]
        @property
        def SQLALCHEMY_DATABASE_URI(self) -> str:
            return "sqlite:///:memory:"

        @computed_field
        @property
        def scoped_engine(self) -> bool: return True


settings = Settings()
