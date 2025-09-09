from django import forms

from .models import CustomUser


class RegisterForm(forms.ModelForm):
    repeat_password = forms.CharField(max_length=90, min_length=8, required=True, widget=forms.PasswordInput, label="Повтор пароля")

    def clean_repeat_password(self) -> dict | None:
        cd = self.cleaned_data
        if cd["repeat_password"] == cd["password"]:
            return cd
        raise forms.ValidationError("Пароли не совпадают")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "birthday", "bio", "password"]
        widgets = {"password": forms.PasswordInput()} # add date choice in form (?: "birthday": forms.DateInput())