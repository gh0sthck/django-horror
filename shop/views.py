from django.shortcuts import render
from django.views.generic.list import ListView

from shop.models import Product


class MainShop(ListView):
    model = Product
    context_object_name = "products"
    template_name = "shop/products_list.html"