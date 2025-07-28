import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfstorage.settings')

import django
django.setup()

from selfstorage_db.models import Client, Warehouse, StorageUnit
from django.utils import timezone


def create_or_update_client(
        user_id, full_name=None,
        phone_number=None, address=None,
        is_legal=False):
    """Создает или обновляет клиента в базе данных"""
    defaults = {
        'is_legal': is_legal
    }

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
    """Покажет арендованные боксы/стеллажи"""
    try:
        client = Client.objects.get(user_id=user_id)
        units = client.rented_units.filter(is_available=False).select_related('warehouse')

        if not units:
            return "У вас нет арендованных ячеек."

        result = []
        for unit in units:
            warehouse = unit.warehouse
            remaining_days = (unit.end_rent_date - timezone.now().date()).days if unit.end_rent_date else 0

            if unit.size == 'RACK':
                unit_type = f"Стеллаж для документов (№{unit.unit_number})"
            else:
                unit_type = f"{unit.get_size_display()} (№{unit.unit_number})"

            unit_info = (
                f"📍 Адрес склада: {warehouse.address}\n"
                f"📦 Тип: {unit_type}\n"
                f"⏳ Срок аренды: до {unit.end_rent_date.strftime('%d.%m.%Y') if unit.end_rent_date else 'не указан'}\n"
                f"⌛ Осталось дней: {remaining_days if remaining_days > 0 else 'срок истёк'}\n"
                f"💳 Стоимость: {unit.price} руб./мес\n"
                f"----------------------------------"
            )
            result.append(unit_info)

        header = f"📊 Ваши арендованные единицы хранения ({len(units)}):\n\n"
        return header + "\n\n".join(result)

    except Client.DoesNotExist:
        return "У вас нет арендованных ячеек."


def get_warehouses(is_legal=False):
    """Получает склады с доступными единицами хранения"""
    warehouses = []
    for w in Warehouse.objects.all():
        if is_legal:
            if w.available_racks > 0:
                warehouses.append([f"{w.name} - {w.address}"])
        else:
            if w.available_boxes > 0:
                warehouses.append([f"{w.name} - {w.address}"])
    return warehouses


def get_available_sizes(warehouse_id=None, is_legal=False):
    """Получает доступные единицы хранения из БД"""
    if is_legal:
        # Юр лицо
        if not warehouse_id:
            return []

        try:
            available_racks = StorageUnit.objects.filter(
                warehouse_id=warehouse_id,
                size='RACK',
                is_available=True
            ).order_by('unit_number')

            return [f"Стеллаж №{rack.unit_number}" for rack in available_racks]
        except Exception as e:
            print(f"Ошибка при получении стеллажей: {e}")
            return []
    else:
        # Физ лицо
        filter_args = {
            'is_available': True,
            'size__in': ['S', 'M', 'L', 'XL']
        }
        if warehouse_id:
            filter_args['warehouse_id'] = warehouse_id

        try:
            available_cells = StorageUnit.objects.filter(**filter_args)\
                               .order_by('size', 'unit_number')

            size_groups = {}
            for cell in available_cells:
                size_name = cell.get_size_display()
                if size_name not in size_groups:
                    size_groups[size_name] = []
                size_groups[size_name].append(cell.unit_number)

            result = []
            for size, numbers in size_groups.items():
                for num in numbers:
                    result.append(f"{size} (№{num})")

            return result
        except Exception as e:
            print(f"Ошибка при получении ячеек: {e}")
            return []
