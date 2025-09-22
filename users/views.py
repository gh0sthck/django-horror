from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, ListView
from django import forms
from django.http import Http404

from posts.models import Post
from users.models import CustomUser

from .forms import RegisterForm


class RegisterView(FormView):
    template_name = "users/register.html"
    success_url = reverse_lazy("main")
    form_class = RegisterForm

    def form_valid(self, form: forms.Form):
        new_user: CustomUser = form.save(commit=False)
        new_user.set_password(new_user.password)
        new_user.save()
        return redirect("main")


class ProfileView(DetailView):
    model = CustomUser
    context_object_name = "user"
    template_name = "users/profile.html"


# Can be private or not
class ProfileFavoritesList(View):
    def get(self, request: HttpRequest, slug):
        user: CustomUser = CustomUser.objects.filter(slug=slug)
        user_favs = []
        if user:
            user_favs = [p for p in user[0].favorites.all()]
            return render(request, "users/favorites.html", {"favs": user_favs})
        raise Http404("Такого пользователя не существует")