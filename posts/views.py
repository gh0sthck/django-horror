from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView, DeleteView
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
            print("FAVS: ", self.request.user.favorites.all())
        if request.GET.get("not_favorite") == "nfv":
            self.request.user.remove_from_favorites(self.get_object())
            print("FAVS: ", self.request.user.favorites.all())
        
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


# login required (!)
class UpdatePostView(UpdateView):
    model = Post
    context_object_name = "post"
    fields = ["title", "text", "description"]
    template_name = "posts/update_post.html"
    success_url = reverse_lazy("main")


# login required (!)
class DeletePostView(DeleteView):
    model = Post
    context_object_name = "post"
    template_name = "posts/delete_post.html"
    success_url = reverse_lazy("main")
