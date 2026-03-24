from django import forms

from blog.models import BlogNote
from posts.models import Comments


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = BlogNote
        fields = ["title", "cover", "text", "is_news"]
        
    def delete_news(self):
        self.fields.pop("is_news")
       
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {"comment": forms.Textarea(attrs={"placeholder": "Оставьте свой комментарий..."})}
