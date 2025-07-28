import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfstorage.settings')

import django
django.setup()

from selfstorage_db.models import Client, Warehouse
from django.utils import timezone


def create_or_update_client(user_id, full_name=None, phone_number=None, address=None):
    """Создает или обновляет клиента в базе данных"""
    defaults = {}

    if full_name is not None:
        defaults['full_name'] = full_name
    if phone_number is not None:
        defaults['phone_number'] = phone_number
    if address is not None:
        defaults['address'] = address

    client, created = Client.objects.update_or_create(
        user_id=user_id,
        defaults=defaults
    )
    return client


def get_my_storages(user_id):
    """Покажет арендованные боксы и их отсутствие"""
    try:
        client = Client.objects.get(user_id=user_id)
        boxes = client.boxes.filter(is_available=False).select_related('warehouse')

        if not boxes:
            return "У вас нет арендованных ячеек."

        result = []
        for box in boxes:
            warehouse = box.warehouse
            remaining_days = (box.end_rent_date - timezone.now()).days if box.end_rent_date else 0

            box_info = (
                f"📍 Адрес склада: {warehouse.address}\n"
                f"📦 Бокс: {box.get_size_display()} (№{box.num})\n"
                f"⏳ Срок аренды: до {box.end_rent_date.strftime('%d.%m.%Y') if box.end_rent_date else 'не указан'}\n"
                f"⌛ Осталось дней: {remaining_days if remaining_days > 0 else 'срок истёк'}\n"
                f"💳 Стоимость: {box.price} руб./мес\n"
                f"----------------------------------"
            )
            result.append(box_info)

        header = f"📊 Ваши арендованные ячейки ({len(boxes)}):\n\n"
        return header + "\n\n".join(result)

    except Client.DoesNotExist:
        return "У вас нет арендованных ячеек."


def get_warehouses():
    """Получаем все склады из базы в формате: ['Название - Адрес']"""
    return [[f"{w.name} - {w.address}"] for w in Warehouse.objects.all()]
