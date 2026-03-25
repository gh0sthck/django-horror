from django import forms
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, UpdateView, DeleteView
from django_ckeditor_5.widgets import CKEditor5Widget

from blog.forms import CommentForm, CreateNoteForm
from blog.models import BlogNote
from posts.models import Comments
from users.models import CustomUser
from utils.auth import ClassLoginRequired, authenticate_required


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
    form = CommentForm
    
    @authenticate_required
    def post(self, *args, **kwargs):
        f: CommentForm = self.form(self.request.POST)
        if f.is_valid():
            data: Comments = f.save(commit=False)
            data.user = self.request.user
            data.save()
            
            note: BlogNote = self.get_object()
            if self.request.POST.get("answer_to"):
                answer_to_comment: Comments = Comments.objects.get(id=self.request.POST.get("answer_to"))
                answer_to_comment.answer.add(data) 
            else: 
                note.comments.add(data)
            return redirect("specific_note", slug=note.slug)
        return self.form()
    
    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data["form"] = self.form() 
        return data


class EditNoteView(ClassLoginRequired, UpdateView):
    model = BlogNote
    fields = ["title", "cover", "text", "is_news"]
    context_object_name = "note"
    template_name = "blog/edit_note.html"
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


class CreateNoteView(ClassLoginRequired, FormView):
    form = CreateNoteForm
    template_name = "blog/edit_note.html"
    success_url = reverse_lazy("main")
    form_class = CreateNoteForm
    
    def form_valid(self, form: CreateNoteForm):
        data: BlogNote = form.save(commit=False)
        data.author = self.request.user
        data.save()
        return super().form_valid(form)
    
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


class DeleteNoteView(ClassLoginRequired, DeleteView):
    model = BlogNote
    success_url = reverse_lazy("main")
    template_name = "blog/delete_note.html"
    context_object_name = "note"
