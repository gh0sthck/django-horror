from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
from django import forms
from django.core.paginator import Paginator
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.models import BlogNote
from posts.forms import CreatePostForm
from posts.models import Category, Post, Comments, Tag
from posts.forms import CommentForm



class MainPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        stories = Post.objects.all()[:4]
        news = BlogNote.objects.filter(is_news=True)[:5]
        return render(request, "posts/main.html", {"stories": stories, "news": news})


class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"
    form = CommentForm

    def get_comments(self) -> list[Comments | dict[Comments, list]]:
        def solution(
            comments: list[Comments], ls: list = []
        ) -> list[Comments | dict[Comments, list]]:
            """
            result:
            [
                Model,
                Model,
                {
                    Model: [
                            Model,
                            Model,
                            {Model: Model, ...},
                            Model, ...
                            ],
                },
                Model
            ]
            """
            for comment in comments:
                if len(comment.answer.all()) == 0:
                    ls += [comment]
                else:
                    ls += [{comment: solution(comment.answer.all(), [])}]
            return ls

        return solution(self.get_object().comments.all(), [])

    # login_required (!)
    def post(self, *args, **kwargs):
        f: CommentForm = self.form(self.request.POST)
        if f.is_valid():
            data: Comments = f.save(commit=False)
            data.user = self.request.user
            data.save()
            post: Post = self.get_object()
            post.comments.add(data)
            return redirect("specific_post", slug=post.slug)
        return self.form()


    def get(self, request: HttpRequest, *args, **kwargs):
        if request.GET.get("is_favorite") == "fv":
            self.request.user.add_to_favorites(self.get_object())
        if request.GET.get("not_favorite") == "nfv":
            self.request.user.remove_from_favorites(self.get_object())
        
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data: dict = super().get_context_data(**kwargs)
        data["form"] = self.form()
        data["comms"] = self.get_comments()
        return data


# login required (!)
class CreatePostView(FormView):
    form_class = CreatePostForm
    success_url = reverse_lazy("main")
    template_name = "posts/create_post.html"

    def form_valid(self, form: forms.Form):
        post: Post = form.save(commit=False)
        post.author = self.request.user
        post.save()
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


# login required (!)
class UpdatePostView(UpdateView):
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

# login required (!)
class DeletePostView(DeleteView):
    model = Post
    context_object_name = "post"
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy("main")


class ReadView(View):
    def get(self, request: HttpRequest):
        posts = Post.objects.all()
        url = ""
        q = None
        categories = Category.objects.all()
        tags = Tag.objects.all()
        tg = [tag for tag in tags if tag.name in request.GET.getlist("tags")]
        cats = [cat for cat in categories if cat.name in request.GET.getlist("cat")] 
        
        # Search filter
        """if request.GET.get("q") and tg:
            q = request.GET.get("q")
            posts = Post.objects.filter(title__contains=q, tags__in=tg)  # iexact don't work - sqlite issue? change to postgres
        elif request.GET.get("q"):
            q = request.GET.get("q")
            posts = Post.objects.filter(title__contains=q) 
        else:
            posts = Post.objects.filter(tags__in=tg) 
         
        cats = [cat for cat in Category.objects.all() if cat.name in request.GET.getlist("cat")]

        if cats:
            posts = [post for post in posts if post.category in cats] """
       
        if request.GET.get("q") and cats and tg:
            q = request.GET.get("q")
            posts = [post for post in Post.objects.filter(title__contains=q, tags__name__in=tg, category__name__in=cats)]
            url = "?" + "&".join("cat="+c.name for c in cats) + "&".join("tags="+t.name for t in tg) + f"&q={q}" + "&page="
        elif request.GET.get("q") and cats:
            q = request.GET.get("q")
            posts = [post for post in Post.objects.filter(title__contains=q, category__name__in=cats)]
            url = "?" + "&".join("cat="+c.name for c in cats) + f"&q={q}" + "&page="
        elif request.GET.get("q") and tg:
            q = request.GET.get("q")
            posts = [post for post in Post.objects.filter(title__contains=q, tags__name__in=tg)]
            url = "?" + "&".join("tags="+t.name for t in tg) + f"&q={q}" + "&page="
        elif tg and cats:
            posts = [post for post in Post.objects.filter(tags__name__in=tg, category__name__in=cats)]
            url = "?" + "&".join("cat="+c.name for c in cats) + "&".join("tags="+t.name for t in tg) + "&page="
        elif tg:
            posts = [post for post in Post.objects.filter(tags__name__in=tg)] 
            url = "?" + "&".join("tags="+t.name for t in tg) + "&page="
        elif cats:
            posts = [post for post in Post.objects.filter(category__name__in=cats)]
            url = "?" + "&".join("cat="+c.name for c in cats) + "&page="
        elif request.GET.get("q"):
            q = request.GET.get("q")
            posts = [post for post in Post.objects.filter(title__contains=q)]
            url = f"?q={q}&page="
        else:
            url = "?page="
        
        
        all_posts_count = len(posts)
        
        paginator = Paginator(posts, 6)
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
            }
        )
