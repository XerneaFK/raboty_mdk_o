from django.contrib import admin
from .models import Category, Dish, DiningTable, Order, OrderItem

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(DiningTable)
admin.site.register(Order)
admin.site.register(OrderItem)
