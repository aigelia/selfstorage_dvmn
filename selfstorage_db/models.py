from django.db import models

from datetime import time

# Create your models here.


class Client(models.Model):
    user_id = models.IntegerField(verbose_name="id")
    full_name = models.CharField("ФИО", max_length=100, null=True, blank=True)
    phone_number = models.CharField(
        "номер телефона",
        max_length=10,
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="адрес"
    )

    def __str__(self):
        return f"{self.user_id}, ({self.full_name})"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name="название склада")
    address = models.CharField(max_length=100, verbose_name="адрес")
    open_time = models.TimeField("open_time", default=time(7, 0))
    close_time = models.TimeField("close_time", default=time(19, 0))
    total_boxes_size_s = models.PositiveIntegerField(verbose_name="боксы размера S", default=0)
    total_boxes_size_m = models.PositiveIntegerField(verbose_name="боксы размера M", default=0)
    total_boxes_size_l = models.PositiveIntegerField(verbose_name="боксы размера L", default=0)
    available_boxes_s = models.PositiveIntegerField(verbose_name="доступные боксы S", default=0)
    available_boxes_m = models.PositiveIntegerField(verbose_name="доступные боксы M", default=0)
    available_boxes_l = models.PositiveIntegerField(verbose_name="доступные боксы L", default=0)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Box(models.Model):
    sizes = [
        ("S", "1 м3"),
        ("M", "5 м3"),
        ("L", "10 м3")
    ]
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="boxes",
        verbose_name="клиент"
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.CASCADE,
        related_name="boxes",
        verbose_name="склад"
    )
    num = models.CharField(max_length=10, verbose_name="номер бокса")
    size = models.CharField(max_length=2, choices=sizes, verbose_name="размер бокса")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="цена аренды в месяц")
    is_available = models.BooleanField(default=True, verbose_name="доступен для аренды")
    start_rent_date = models.DateTimeField(null=True, blank=True, verbose_name="начало аренды")
    end_rent_date = models.DateTimeField(null=True, blank=True, verbose_name="конец аренды")

    def __str__(self):
        return f"Бокс №{self.num} {self.get_size_display()}\
            {self.warehouse.name} - {self.warehouse.address}"

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"
