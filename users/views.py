from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from django import forms

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
    pass