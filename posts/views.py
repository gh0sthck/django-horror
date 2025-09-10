from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView
from django import forms

from posts.forms import CreatePostForm
from posts.models import Post, Comments
from posts.forms import CommentForm
 

class MainPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        stories = Post.objects.all()[:5]
        return render(request, "posts/main.html", {"stories": stories})


class PostView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post.html"
    form = CommentForm

    # login_required (!)
    def post(self, *args, **kwargs):
        f: CommentForm = self.form(self.request.POST)
        if f.is_valid():
            print("FORM IS VALID")
            data: Comments = f.save(commit=False)
            
            data.user = self.request.user
            # fix saves - comments not create
            data.save_base()
            print(data.__dict__)
            return redirect("main")
        return self.form()

    def get_context_data(self, **kwargs):
        data: dict = super().get_context_data(**kwargs)
        data["form"] = self.form()
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