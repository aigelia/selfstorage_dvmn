from selfstorage_db.models import Client
from django.utils import timezone


def create_client(user_id, full_name, phone_number=None, address=None):
    Client.objects.create(
        user_id=user_id, full_name=full_name,
        phone_number=phone_number, address=address
    )


def get_my_storages(user_id):  # из бд
    """Покажет арендованные боксы и их отсутствие"""
    client = Client.objects.filter(user_id=user_id).first()
    if not client:
        return "У вас нет арендованных ячеек."

    boxes = client.boxes.filter(is_available=False).select_related('warehouse')
    if not boxes:
        return "У вас нет арендованных ячеек."

    result = []
    for box in boxes:
        warehouse = box.warehouse
        remaining_days = (box.end_rent_date - timezone.now()).days if box.end_rent_date else 0

        box_info = (
            f"📍 Адрес склада: {warehouse.address}\n"
            f"📦 Бокс : {box.get_size_display()} (№{box.num})\n"
            f"⏳ Срок аренды: до {box.end_rent_date.strftime('%d.%m.%Y') if box.end_rent_date else 'не указан'}\n"
            f"⌛ Осталось дней: {remaining_days if remaining_days > 0 else 'срок истёк'}\n"
            f"💳 Стоимость: {box.price} руб./мес\n"
            f"----------------------------------"
        )
        result.append(box_info)

    header = f"📊 Ваши арендованные ячейки ({len(boxes)}):\n\n"
    return header + "\n\n".join(result)
