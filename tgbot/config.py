from pydantic_settings import BaseSettings
from pydantic import SecretStr


class PostgresSettings(BaseSettings):
    user: str
    password: SecretStr
    db: str
    host: str = "db"
    port: int = 5432

    @property
    def async_url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    url: str = "redis://redis:6379/0"


class BotSettings(BaseSettings):
    token: SecretStr
    admin_id: int = 502545728
    username: str
    channel_id: int = -1002068510571


class AppSettings(BaseSettings):
    trial_days: int = 14  # длительность пробного периода в днях
    debug: bool = False

    postgres: PostgresSettings
    redis: RedisSettings
    bot: BotSettings

    class Config:
        env_file = ".env"
        env_nested_delimiter = '__'


settings = AppSettings()
