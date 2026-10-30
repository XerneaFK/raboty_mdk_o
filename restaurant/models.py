from django.db import models


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField("Название", max_length=100)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    weight = models.PositiveIntegerField("Вес, г")
    description = models.TextField("Описание", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="dishes",
        verbose_name="Категория",
    )

    def __str__(self):
        return self.name


class DiningTable(models.Model):
    number = models.PositiveIntegerField("Номер столика", unique=True)
    seats = models.PositiveIntegerField("Количество мест")
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=[("Свободен", "Свободен"), ("Занят", "Занят")],
        default="Свободен",
    )

    def __str__(self):
        return f"Столик №{self.number}"


class Order(models.Model):
    table = models.ForeignKey(
        DiningTable,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="Столик",
    )
    date = models.DateTimeField("Дата", auto_now_add=True)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=[
            ("Новый", "Новый"),
            ("Готовится", "Готовится"),
            ("Выполнен", "Выполнен"),
        ],
        default="Новый",
    )
    total = models.DecimalField("Сумма", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    dish = models.ForeignKey(
        Dish,
        on_delete=models.PROTECT,
        verbose_name="Блюдо",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return f"{self.dish} x {self.quantity}"
