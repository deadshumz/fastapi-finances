from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None
    pg_dsn: PostgresDsn | None = None

    @field_validator("pg_dsn", mode="before")
    def build_pg_dsn(cls, v: str | None, fields) -> str:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=fields.data["DB_USER"],
            password=fields.data["DB_PASSWORD"],
            host=fields.data["DB_HOST"],
            port=fields.data["DB_PORT"],
            path=fields.data["DB_NAME"],
        )


settings = Settings()
