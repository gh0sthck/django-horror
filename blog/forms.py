from django import forms

from blog.models import BlogNote


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = BlogNote
        fields = ["title", "cover", "text", "is_news"]
        
    def delete_news(self):
        self.fields.pop("is_news")