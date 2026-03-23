from django.urls import path

from .views import MainShop

urlpatterns = [
    path("", MainShop.as_view(), name="mainshop"),
]