import asyncio

import nats
from nats.aio.client import Client
from nats.js.api import StreamConfig
from nats.js.client import JetStreamContext


async def delayed_stream(js: JetStreamContext):
    # Настройка стрима с заданными параметрами
    stream_config = StreamConfig(
        name="broadcast_messages_aiogram",  # Название стрима
        description=None,  # Описание стрима
        subjects=[
            "aiogram.broadcast.messages",
        ],
        retention="limits",  # Политика удержания
        max_consumers=-1,  # Неограниченное количество потребителей
        max_msgs=-1,  # Неограниченное количество сообщений
        max_bytes=300 * 1024 * 1024,  # 300 MiB
        discard="old",  # Политика удаления
        max_age=None,  # Неограниченный возраст сообщений
        max_msgs_per_subject=-1,  # Неограниченное количество сообщений на тему
        max_msg_size=10 * 1024 * 1024,  # 10 MiB
        storage="file",  # Хранение сообщений на диске
        num_replicas=1,  # Количество реплик стрима
        no_ack=False,  # Требуется явное подтверждение обработки
        template_owner=None,  # Можно указать название шаблона, которому принадлежит стрим
        duplicate_window=2 * 60,  # 2 минуты
        placement=None,  # Правило размещения стрима на узлах кластера
        mirror=None,  # Параметр, определяющий будет ли стрим зеркалом другого стрима
        sources=None,  # Используется для агрегации данных из нескольких стримов в один
        sealed=False,  # Стрим открыт для добавления новых данных
        deny_delete=False,  # Разрешение удалять сообщения
        deny_purge=False,  # Разрешение очищать сабджекты или весь стрим
        allow_rollup_hdrs=False,  # Запрет на "сворачивание сообщений"
        republish=None,  # Настройка перепубликации сообщений в другие темы
        subject_transform=None,  # Позволяет изменять тему сообщения на основе правил
        allow_direct=True,  # Разрешение получать сообщения без создания консьюмера
        mirror_direct=None,  # Настройка разрешения публикации в зеркальный стрим без консьюмера
        compression=None,  # Настройка сжатия сообщений в стриме
        metadata=None  # Метаданные стрима
    )

    await js.add_stream(stream_config)
    print("Stream `DelayedStream` created successfully.")
