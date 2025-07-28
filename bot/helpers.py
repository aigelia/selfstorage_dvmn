from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


def get_next_week_dates_keyboard(callback_prefix):
    today = datetime.today()
    keyboard = []
    for i in range(7):
        day = today + timedelta(days=i)
        date_str = day.strftime('%d.%m.%Y')
        callback_data = f"{callback_prefix}_{day.strftime('%Y-%m-%d')}"
        keyboard.append([InlineKeyboardButton(date_str, callback_data=callback_data)])
    return InlineKeyboardMarkup(keyboard)


def build_summary(user_data: dict) -> str:
    is_legal = user_data.get('is_legal', False)
    name = user_data.get('user_name', '—')
    address = user_data.get('delivery_address', None)
    delivery_text = address if address else 'Самостоятельная доставка'

    storage_type = user_data.get('cell_size', '—')
    rental_period = user_data.get('rental_period', '—')
    start_date = user_data.get('rental_start_date', '—')

    return (
        f"📦 <b>Заявка на хранение</b>\n\n"
        f"👤 Имя: {name}\n"
        f"🏠 Доставка: {delivery_text}\n"
        f"📐 Размер: {storage_type}\n"
        f"⏳ Срок: {rental_period}\n"
        f"📅 Начало: {start_date}\n"
        f"\n❗️Нажмите <i>Подтвердить</i>, чтобы завершить оформление."
    )


def to_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d").date()

