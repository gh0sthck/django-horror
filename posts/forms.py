from django import forms

from posts.models import Post, Comments


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "description", "text", "cover", "category", "tags"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ["comment"]
        widgets = {"comment": forms.Textarea(attrs={"placeholder": "Оставьте свой комментарий..."})}
