from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView
from django import forms
from django.http import Http404
from django.core.paginator import Paginator

from blog.models import BlogNote
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
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paginator = Paginator(BlogNote.objects.filter(author=self.get_object()), 4)
        current_page = self.request.GET.get("page") if self.request.GET.get("page") else "1"
        posts_per_page = paginator.get_page(int(current_page))
        pages_cnt = paginator.num_pages
        ctx["blog_notes"] = posts_per_page
        ctx["pages"] = pages_cnt
        ctx["url"] = "?page="
        return ctx

    def post(self, request: HttpRequest, slug):
        user: CustomUser = self.request.user
        current_user: CustomUser = self.get_object()
        if request.POST["sub"] == "1":
            user.follow_user(current_user)
        if request.POST["sub"] == "0":
            user.unfollow_user(current_user)
        return redirect("profile", slug=slug)
        


# Can be private or not
class ProfileFavoritesList(View):
    def get(self, request: HttpRequest, slug):
        user: CustomUser = CustomUser.objects.filter(slug=slug)
        user_favs = []
        if user:
            user_favs = [p for p in user[0].favorites.all()]
            return render(
                request, 
                "users/favorites.html", 
                {
                    "favs": user_favs, 
                    "user": user[0],
                }
            )
        raise Http404("Такого пользователя не существует")
