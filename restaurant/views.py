from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Dish, Category, DiningTable, Order, OrderItem


def menu(request):
    dishes = Dish.objects.all().order_by("name")
    category_id = request.GET.get("category")

    if category_id:
        dishes = dishes.filter(category_id=category_id)

    categories = Category.objects.all().order_by("name")
    return render(request, "restaurant/menu.html", {
        "dishes": dishes,
        "categories": categories,
    })


def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    return render(request, "restaurant/dish_detail.html", {"dish": dish})


def create_order(request):
    if request.method == "POST":
        table_id = request.POST.get("table")
        dish_id = request.POST.get("dish")
        quantity = int(request.POST.get("quantity", 1))

        if quantity < 1:
            return HttpResponse("Количество должно быть больше нуля.", status=400)

        table = get_object_or_404(DiningTable, pk=table_id)
        dish = get_object_or_404(Dish, pk=dish_id)

        order = Order.objects.create(table=table, total=dish.price * quantity)
        OrderItem.objects.create(order=order, dish=dish, quantity=quantity)
        table.status = "Занят"
        table.save()

        return render(request, "restaurant/order_success.html", {"order": order})

    return render(request, "restaurant/order_form.html", {
        "dishes": Dish.objects.all().order_by("name"),
        "tables": DiningTable.objects.filter(status="Свободен").order_by("number"),
    })
