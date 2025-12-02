from tokenize import Comment
from django import forms

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    repeat_password = forms.CharField(
        max_length=90,
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "Повтор пароля"}),
        label="Повтор пароля",
    )

    def clean_repeat_password(self) -> dict | None:
        cd = self.cleaned_data
        if cd["repeat_password"] == cd["password"]:
            return cd
        raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = CustomUser
        fields = ["username", "avatar", "email", "birthday", "bio", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Имя пользователя"}),
            "email": forms.EmailInput(attrs={"placeholder": "Электронная почта"}),
            "avatar": forms.FileInput(attrs={"placeholder": "Аватар"}),
            "bio": forms.Textarea(attrs={"placeholder": "Напишите пару слов о себе: чем увлекаетесь, что пишите или что читаете!"}),
            "birthday": forms.DateInput(attrs={"placeholder": "Дата рождения"}),
            "password": forms.PasswordInput(attrs={"placeholder": "Пароль"}),
        }  # add date choice in form (?: "birthday": forms.DateInput())
