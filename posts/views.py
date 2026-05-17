from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from django import forms
from django.core.paginator import Paginator
from django_ckeditor_5.widgets import CKEditor5Widget
from django.utils.timezone import make_aware

from blog.models import BlogNote
from core.redis_c import get_redis_connection
from posts.forms import CreatePostForm
from posts.models import Category, Post, Comments, Tag
from posts.forms import CommentForm
from utils.auth import ClassLoginRequired, authenticate_required


class MainPage(View):
    def stories_sort(self, stories: list[Post]):
        nl = []
        for story in stories:
            likes, views = story.get_likes_count(), story.get_views_count()
            nl.append((story, likes+views))
           
        nl.sort(key=lambda x: x[1], reverse=True) 
        return [story[0] for story in nl] 
         
    def get(self, request: HttpRequest) -> HttpResponse:
        tz = ZoneInfo("Europe/Moscow")
        stories = Post.objects.filter(created_date__gt=make_aware(datetime.now()-timedelta(days=7), tz))
        news = BlogNote.objects.filter(is_news=True).order_by("-pubdate")[:5]
        return render(request, "posts/main.html", {"stories": self.stories_sort(stories)[:4], "news": news})


class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"
    form = CommentForm
    r_conn = get_redis_connection()

    @authenticate_required
    def post(self, request: HttpRequest, *args, **kwargs):
        if request.POST.get("lk") == "lk":
            self.get_object().set_like(request.user.id)
            return redirect("specific_post", slug=self.get_object().slug)
        elif request.POST.get("nlk") == "nlk":
            self.get_object().remove_like(request.user.id)
            return redirect("specific_post", slug=self.get_object().slug)
        else:
            f: CommentForm = self.form(self.request.POST)
            if f.is_valid():
                data: Comments = f.save(commit=False)
                data.user = self.request.user
                data.save()

                post: Post = self.get_object()
                if self.request.POST.get("answer_to"):
                    answer_to_comment: Comments = Comments.objects.get(
                        id=self.request.POST.get("answer_to")
                    )
                    answer_to_comment.answer.add(data)
                else:
                    post.comments.add(data)
                return redirect("specific_post", slug=post.slug)
            return self.form()

    def check_view(self, request: HttpRequest):
        if request.user.is_authenticated:
            if not self.get_object().check_view(request.user.id):
                self.get_object().set_view(request.user.id)

    def get(self, request: HttpRequest, *args, **kwargs):
        self.check_view(request=request)
        if request.GET.get("is_favorite") == "fv":
            self.request.user.add_to_favorites(self.get_object())
        if request.GET.get("not_favorite") == "nfv":
            self.request.user.remove_from_favorites(self.get_object())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data: dict = super().get_context_data(**kwargs)
        data["form"] = self.form()
        data["is_liked"] = (
            self.get_object().check_like(self.request.user.id)
            if self.request.user.is_authenticated
            else False
        )
        return data


class CreatePostView(ClassLoginRequired, FormView):
    form_class = CreatePostForm
    success_url = reverse_lazy("main")
    template_name = "posts/create_post.html"

    def form_valid(self, form: forms.Form):
        post: Post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        form.save_m2m()
        return redirect("specific_post", slug=post.slug)

    def get_form_class(self):
        form: forms.Form = super().get_form_class()
        for field in form.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            if isinstance(field.widget, forms.widgets.ClearableFileInput):
                field.widget = forms.widgets.FileInput()
            else:
                if not isinstance(field.widget, CKEditor5Widget):
                    field.widget.attrs["class"] = "post_create_input"

        return form


class UpdatePostView(ClassLoginRequired, UpdateView):
    model = Post
    context_object_name = "post"
    fields = ["title", "text", "description", "cover", "category", "tags"]
    template_name = "posts/create_post.html"
    success_url = reverse_lazy("main")

    def get_form_class(self):
        form: forms.Form = super().get_form_class()
        for field in form.base_fields.values():
            field.widget.attrs["placeholder"] = field.label
            if isinstance(field.widget, forms.widgets.ClearableFileInput):
                field.widget = forms.widgets.FileInput()
            else:
                if not isinstance(field.widget, CKEditor5Widget):
                    field.widget.attrs["class"] = "post_create_input"
        return form

    def get_context_data(self, **kwargs):
        cd: dict = super().get_context_data(**kwargs)
        cd["is_editing"] = True
        return cd


class DeletePostView(ClassLoginRequired, DeleteView):
    model = Post
    context_object_name = "post"
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy("main")

    def post(self, request, *args, **kwargs):
        r_conn = get_redis_connection()
        print("DELETING")
        r_conn.delete(f"pl_{self.get_object().pk}", f"pv_{self.get_object().pk}")
        try: 
            a = r_conn.lrange(f"pl{self.get_object().pk}", 0, -1) 
        except Exception:
            print("error") 
        return super().post(request, *args, **kwargs)


class ReadView(View):
    def get(self, request: HttpRequest):
        posts = Post.objects.all()
        url = ""
        q = None
        categories = Category.objects.all()
        tags = Tag.objects.all()
        tg = [tag for tag in tags if tag.name in request.GET.getlist("tags")]
        cats = [cat for cat in categories if cat.name in request.GET.getlist("cat")]

        if request.GET.get("q") and cats and tg:
            q = request.GET.get("q")
            posts = [
                post
                for post in Post.objects.filter(
                    title__contains=q, tags__name__in=tg, category__name__in=cats
                )
            ]
            url = (
                "?"
                + "&".join("cat=" + c.name for c in cats)
                + "&".join("tags=" + t.name for t in tg)
                + f"&q={q}"
                + "&page="
            )
        elif request.GET.get("q") and cats:
            q = request.GET.get("q")
            posts = [
                post
                for post in Post.objects.filter(
                    title__contains=q, category__name__in=cats
                )
            ]
            url = "?" + "&".join("cat=" + c.name for c in cats) + f"&q={q}" + "&page="
        elif request.GET.get("q") and tg:
            q = request.GET.get("q")
            posts = [
                post
                for post in Post.objects.filter(title__contains=q, tags__name__in=tg)
            ]
            url = "?" + "&".join("tags=" + t.name for t in tg) + f"&q={q}" + "&page="
        elif tg and cats:
            posts = [
                post
                for post in Post.objects.filter(
                    tags__name__in=tg, category__name__in=cats
                )
            ]
            url = (
                "?"
                + "&".join("cat=" + c.name for c in cats)
                + "&".join("tags=" + t.name for t in tg)
                + "&page="
            )
        elif tg:
            posts = [post for post in Post.objects.filter(tags__name__in=tg).distinct()]
            url = "?" + "&".join("tags=" + t.name for t in tg) + "&page="
        elif cats:
            posts = [post for post in Post.objects.filter(category__name__in=cats).distinct()]
            url = "?" + "&".join("cat=" + c.name for c in cats) + "&page="
        elif request.GET.get("q"):
            q = request.GET.get("q")
            posts = [post for post in Post.objects.filter(title__contains=q).distinct()]
            url = f"?q={q}&page="
        else:
            url = "?page=" 

        all_posts_count = len(posts)

        paginator = Paginator(posts, 10)
        current_page = request.GET.get("page") if request.GET.get("page") else "1"
        posts_per_page = paginator.get_page(int(current_page))
        pages_count = paginator.num_pages

        return render(
            request,
            "posts/read.html",
            {
                "posts_cnt": all_posts_count,
                "posts": posts_per_page,
                "url": url,
                "pages": pages_count,
                "categories": categories,
                "q": q,
                "tags": tags,
            },
        )
