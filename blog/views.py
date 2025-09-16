from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView, DeleteView

from blog.forms import CreateNoteForm
from blog.models import BlogNote


class NewsView(View):
    pass


class FeedView(View):
    pass


class NoteView(DetailView):
    model = BlogNote
    template_name = "blog/note.html"
    context_object_name = "note"


class EditNoteView(UpdateView):
    model = BlogNote
    template_name = "blog/edit_note.html"
    success_url = reverse_lazy("main")


class CreateNoteView(FormView):
    form = CreateNoteForm
    template_name = "blog/edit_note.html"
    success_url = reverse_lazy("feed")


class DeleteNoteView(DeleteView):
    model = BlogNote
    success_url = reverse_lazy("main")
    template_name = "blog/delete_note.html"
