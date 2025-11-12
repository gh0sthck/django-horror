from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from django import forms
from django.http import Http404
from django.core.paginator import Paginator

from blog.models import BlogNote
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
    

class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = "users/update.html"
    fields = ["username", "birthday", "status", "bio"]
    success_url = reverse_lazy("main")
    
    def get_form_class(self):
        form: forms.Form = super().get_form_class()
        for field in form.base_fields.values():
            field.widget.attrs["class"] = "def_input"
            field.widget.attrs["placeholder"] = str(field.label)
        return form


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
        ctx["followers_len"] = len(CustomUser.objects.filter(blog_following__in=[self.get_object()]))
        ctx["stories_len"] = len(Post.objects.filter(author=self.get_object()))
        return ctx

    def post(self, request: HttpRequest, slug):
        user: CustomUser = self.request.user
        current_user: CustomUser = self.get_object()
        if request.POST["sub"] == "1":
            user.follow_user(current_user)
        if request.POST["sub"] == "0":
            user.unfollow_user(current_user)
        return redirect("profile", slug=slug)


class ProfileSubscribesView(View):
    def get(self, request: HttpRequest, slug):
        user = CustomUser.objects.get(slug=slug)
        subscriptions: list[CustomUser] = user.blog_following.all()
        
        return render(request, "users/subscriptions.html", {
            "user": user,
            "subs": subscriptions,
            "followers_len": len(CustomUser.objects.filter(blog_following__in=[user])),
            "stories_len": len(Post.objects.filter(author=user)),
        })
        

class ProfileFollowersView(View):
    def get(self, request: HttpRequest, slug):
        user = CustomUser.objects.get(slug=slug)
        followers = CustomUser.objects.filter(blog_following__in=[user])
        
        return render(request, "users/subscriptions.html", {
            "user": user,
            "subs": followers,
            "followers_len": len(CustomUser.objects.filter(blog_following__in=[user])),
            "stories_len": len(Post.objects.filter(author=user)),
        })


# Can be private or not
class ProfileFavoritesList(View):
    def get(self, request: HttpRequest, slug):
        user: CustomUser = CustomUser.objects.get(slug=slug)
        user_favs = []
        if user:
            user_favs = [p for p in user.favorites.all()]
            return render(
                request, 
                "users/favorites.html", 
                {
                    "favs": user_favs, 
                    "user": user,
                    "followers_len": len(CustomUser.objects.filter(blog_following__in=[user])),
                    "stories_len": len(Post.objects.filter(author=user))
                }
            )
        raise Http404("Такого пользователя не существует")


class ProfileStoriesView(View):
    def get(self, request: HttpRequest, slug):
        user = CustomUser.objects.get(slug=slug)
        user_stories = Post.objects.filter(author=user)
        
        return render(request, "users/stories.html", {
            "user": user,
            "followers_len": len(CustomUser.objects.filter(blog_following__in=[user])),
            "stories_len": len(user_stories),
            "stories": user_stories,
        })
        

class ProfileDeleteView(DeleteView):
    model = CustomUser
    success_url = reverse_lazy("main")
    template_name = "users/delete.html"
    context_object_name = "del_user"