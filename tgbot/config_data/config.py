from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class Admin:
    admin: str


@dataclass
class Database:
    host: str
    user: str
    password: str
    db_name: str
    port: int | None = None


@dataclass
class NatsConfig:
    servers: list[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class NatsBroadcastConsumerConfig:
    subject: str
    stream: str
    durable_name: str


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig
    broadcast_consumer: NatsBroadcastConsumerConfig
    database: Database
    admin: Admin


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env()
    return Config(
        admin=Admin(env.str('ADMIN')),
        tg_bot=TgBot(token=env.str("BOT_TOKEN")),
        nats=NatsConfig(servers=env.list('NATS_SERVERS')),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject=env('NATS_DELAYED_CONSUMER_SUBJECT'),
            stream=env('NATS_DELAYED_CONSUMER_STREAM'),
            durable_name=env('NATS_DELAYED_CONSUMER_DURABLE_NAME'),
        ),
        broadcast_consumer=NatsBroadcastConsumerConfig(
            subject=env('NATS_BROADCAST_CONSUMER_SUBJECT'),
            stream=env('NATS_BROADCAST_CONSUMER_STREAM'),
            durable_name=env('NATS_BROADCAST_CONSUMER_DURABLE_NAME'),
        ),
        database=Database(
            host=env.str("DB_HOST"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASS"),
            db_name=env.str("DB_NAME")
        )
    )
