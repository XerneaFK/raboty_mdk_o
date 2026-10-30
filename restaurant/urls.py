from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu, name="menu"),
    path("menu/<int:pk>/", views.dish_detail, name="dish_detail"),
    path("orders/create/", views.create_order, name="create_order"),
]
