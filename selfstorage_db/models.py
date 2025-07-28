from django.db import models
from datetime import time


class Client(models.Model):
    user_id = models.IntegerField(verbose_name="id", unique=True)
    full_name = models.CharField("ФИО", max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        "Номер телефона",
        max_length=20,
        blank=True,
        null=True
    )
    address = models.CharField(
        "Адрес",
        max_length=200,
        blank=True,
        null=True
    )
    is_legal = models.BooleanField(
        "Юридическое лицо",
        default=False
    )

    def __str__(self):
        return f"{self.user_id} ({self.full_name or 'Без имени'})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Warehouse(models.Model):
    name = models.CharField("Название склада", max_length=100)
    address = models.CharField("Адрес", max_length=200)
    open_time = models.TimeField("Время открытия", default=time(9, 0))
    close_time = models.TimeField("Время закрытия", default=time(18, 0))

    # физ лицо
    total_boxes = models.PositiveIntegerField("Общее количество ячеек", default=0)
    available_boxes = models.PositiveIntegerField("Доступные ячейки", default=0)

    # юр лицо
    total_racks = models.PositiveIntegerField("Количество стеллажей", default=0)
    available_racks = models.PositiveIntegerField("Доступные стеллажи", default=0)

    def __str__(self):
        return f"{self.name} ({self.address})"

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class StorageUnit(models.Model):
    SIZE_CHOICES = [
        ("S", "Малый (1 м³)"),
        ("M", "Средний (5 м³)"),
        ("L", "Большой (10 м³)"),
        ("XL", "Очень большой (15 м³)"),
        ("RACK", "Стеллаж для документов")
    ]

    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="storage_units",
        verbose_name="Склад"
    )
    unit_number = models.CharField("Номер единицы", max_length=20)
    size = models.CharField(
        "Тип/размер",
        max_length=5,
        choices=SIZE_CHOICES
    )
    price = models.DecimalField(
        "Цена в месяц",
        max_digits=10,
        decimal_places=2
    )
    is_available = models.BooleanField("Доступен", default=True)
    start_rent_date = models.DateField("Начало аренды", null=True, blank=True)
    end_rent_date = models.DateField("Окончание аренды", null=True, blank=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="rented_units",
        verbose_name="Арендатор"
    )

    def __str__(self):
        return f"{self.get_size_display()} №{self.unit_number} ({'Свободен' if self.is_available else 'Занят'})"

    class Meta:
        verbose_name = "Единица хранения"
        verbose_name_plural = "Единицы хранения"
        unique_together = ('warehouse', 'unit_number')
