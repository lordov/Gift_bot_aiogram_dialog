import pandas as pd
import os
from datetime import datetime
from tgbot.database.models import User


async def export_participants_to_excel(participants: list[User]):
    """Экспортирует данные участников в Excel-файл"""
    # Создаем DataFrame из данных участников
    data = []
    for user in participants:
        data.append({
            'ID': user.id,
            'Username': user.username,
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'Participation Number': user.number_of_part,
            'Participation Date': user.last_participation_date.strftime('%Y-%m-%d %H:%M:%S') if user.last_participation_date else '',
            'Total Participations': user.participate
        })

    df = pd.DataFrame(data)

    # Создаем директорию для отчетов, если она не существует
    os.makedirs('reports', exist_ok=True)

    # Формируем имя файла с текущей датой
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_path = f'reports/participants_{current_date}.xlsx'

    # Сохраняем в Excel
    df.to_excel(file_path, index=False)

    return file_path
