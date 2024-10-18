import json
from nats.js.client import JetStreamContext
from datetime import datetime
from tgbot.DB.db import get_all_users


async def publish_broadcast_message(
    js: JetStreamContext,
    message_data: dict,
    subject: str,
    delay: int = 0
):
    # Получаем список пользователей из базы данных
    users = await get_all_users()
    for user in users:
        headers = {
            'Tg-Broadcast-Chat-ID': str(user['chat_id']),
            'Tg-Broadcast-Msg-Timestamp': str(datetime.now().timestamp()),
            'Tg-Broadcast-Msg-Delay': str(delay),
        }
        # В message_data можем хранить текст, фото и URL
        payload = json.dumps(message_data).encode('utf-8')
        await js.publish(subject=subject, payload=payload, headers=headers)
