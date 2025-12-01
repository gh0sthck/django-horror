from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView, DeleteView
from django.db.models import QuerySet

from blog.forms import CreateNoteForm
from blog.models import BlogNote
from users.models import CustomUser


class NewsView(View):
    def get(self, request: HttpRequest):
        admin_notes: list[BlogNote] = list(BlogNote.objects.filter(is_news=True))
        if request.user.is_authenticated:
            current_user: CustomUser = request.user
            following_notes: list[CustomUser] = current_user.blog_following.all()  # Date filter will be add
            for user in following_notes:
                for note in BlogNote.objects.filter(author=user):
                    admin_notes.append(note) if note not in admin_notes else ""
        return render(request, "blog/news.html", {"news": admin_notes})


class UserNotesView(View):
    pass


class NoteView(DetailView):
    model = BlogNote
    template_name = "blog/note.html"
    context_object_name = "note"


class EditNoteView(UpdateView):
    model = BlogNote
    fields = ["title", "cover", "text", "is_news"]
    template_name = "blog/edit_note.html"
    success_url = reverse_lazy("main")


class CreateNoteView(FormView):
    form = CreateNoteForm
    template_name = "blog/edit_note.html"
    success_url = reverse_lazy("main")
    form_class = CreateNoteForm
    
    def form_valid(self, form: CreateNoteForm):
        data: BlogNote = form.save(commit=False)
        data.author = self.request.user
        data.save()
        return super().form_valid(form)
        


class DeleteNoteView(DeleteView):
    model = BlogNote
    success_url = reverse_lazy("main")
    template_name = "blog/delete_note.html"
    context_object_name = "note"
