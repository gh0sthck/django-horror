from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View


class MainPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "test.html")

