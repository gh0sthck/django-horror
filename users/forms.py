from django import forms

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    repeat_password = forms.CharField(max_length=90, min_length=8, required=True, widget=forms.PasswordInput)

    def clean_repeat_password(self) -> dict | None:
        cd = self.cleaned_data
        if cd["repeat_password"] == cd["password"]:
            return cd
        raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "bio", "password"]
        widgets = {"password": forms.PasswordInput()}