import os
from dataclasses import dataclass
from dotenv import load_dotenv


def str_to_bool(value: str | None) -> bool:
    return str(value).lower() in ("1", "true", "yes", "y")


@dataclass(kw_only=True)
class FastAPISettings:
    
    @dataclass(kw_only=True)
    class Cors:
        allow_origins: list[str]
        credentials: bool

    host: str
    port: int
    cors: Cors


@dataclass(kw_only=True)
class GunicornSettings:
    timeout: int
    workers: int


@dataclass(kw_only=True)
class PaginationSettings:
    default_limit: int
    max_limit: int


@dataclass(kw_only=True)
class RedisSettings:
    host: str
    port: int
    db_index: int
    password: str


@dataclass(kw_only=True)
class RabbitMQSettings:
    host: str
    port: int
    user: str
    password: str


@dataclass(kw_only=True)
class PostgresSettings:
    host: str
    port: int
    db: str
    user: str
    password: str
    pool_min_size: int
    pool_max_size: int


@dataclass(kw_only=True)
class Settings:
    gunicorn: GunicornSettings
    fastapi: FastAPISettings
    pagination: PaginationSettings
    redis: RedisSettings
    rabbitmq: RabbitMQSettings
    secret_key: str
    postgres: PostgresSettings
    env: str


class SettingsManager:
    _instance: Settings | None = None

    @classmethod
    def get_config(cls) -> Settings:
        if cls._instance is None:
            load_dotenv()
            cls._instance = cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls) -> Settings:
        return Settings(
            gunicorn=GunicornSettings(
                timeout=int(os.environ.get("GUNICORN_TIMEOUT", 1200)),
                workers=int(os.environ.get("GUNICORN_WORKERS", 1)),
            ),
            fastapi=FastAPISettings(
                host=os.environ.get("FASTAPI_HOST", "0.0.0.0"),
                port=int(os.environ.get("FASTAPI_PORT", 8000)),
                cors=FastAPISettings.Cors(
                    allow_origins=os.environ.get("CORS_ORIGINS", "").split(",") if os.environ.get("CORS_ORIGINS") else [],
                    credentials=str_to_bool(os.environ.get("CORS_CREDENTIALS", "1")),
                ),
            ),
            pagination=PaginationSettings(
                default_limit=int(os.environ.get("PAGINATION_DEFAULT_LIMIT", 20)),
                max_limit=int(os.environ.get("PAGINATION_MAX_LIMIT", 50)),
            ),
            redis=RedisSettings(
                host=os.environ.get("REDIS_HOST", "127.0.0.1"),
                port=int(os.environ.get("REDIS_PORT", 6379)),
                db_index=int(os.environ.get("REDIS_DB_INDEX", 10)),
                password=os.environ.get("REDIS_PASSWORD", ""),
            ),
            rabbitmq=RabbitMQSettings(
                host=os.environ.get("RABBITMQ_HOST", "localhost"),
                port=int(os.environ.get("RABBITMQ_PORT", 5672)),
                user=os.environ.get("RABBITMQ_USER", "guest"),
                password=os.environ.get("RABBITMQ_PASSWORD", "guest"),
            ),
            secret_key=os.environ.get("SECRET_KEY", ""),
            postgres=PostgresSettings(
                host=os.environ.get("POSTGRES_HOST", "localhost"),
                port=int(os.environ.get("POSTGRES_PORT", 5432)),
                db=os.environ.get("POSTGRES_DB", ""),
                user=os.environ.get("POSTGRES_USER", ""),
                password=os.environ.get("POSTGRES_PASSWORD", ""),
                pool_min_size=int(os.environ.get("POSTGRES_MIN_SIZE", 1)),
                pool_max_size=int(os.environ.get("POSTGRES_MAX_SIZE", 10)),
            ),
            env=os.environ.get("ENV", "development"),
        )


settings = SettingsManager.get_config()
