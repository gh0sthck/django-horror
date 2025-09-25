from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView, DeleteView

from blog.forms import CreateNoteForm
from blog.models import BlogNote


class NewsView(View):
    pass


class UserNotesView(View):
    pass


class NoteView(DetailView):
    model = BlogNote
    template_name = "blog/note.html"
    context_object_name = "note"


class EditNoteView(UpdateView):
    model = BlogNote
    fields = ["title", "text"]
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
