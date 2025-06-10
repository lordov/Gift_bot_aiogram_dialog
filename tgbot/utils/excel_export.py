import pandas as pd
import os
from datetime import datetime


async def export_participants_to_excel(participants):
    """Экспортирует данные участников в Excel-файл"""
    # Создаем DataFrame из данных участников
    data = []
    for user, participation in participants:
        data.append({
            'ID': user.id,
            'Username': user.username,
            'First Name': user.first_name,
            'Last Name': user.last_name,
            'Participation Number': participation.participation_number,
            'Participation Date': participation.participation_date.strftime('%Y-%m-%d %H:%M:%S'),
            'Screenshot Verified': 'Да' if participation.screenshot_verified else 'Нет'
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
