from django import forms

from blog.models import BlogNote


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = BlogNote
        fields = ["title", "text"]
