from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=90, verbose_name="Имя пользователя", unique=True, null=False)
    bio = models.TextField(verbose_name="О себе", max_length=256, blank=True, default="")
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    birthday = models.DateField(verbose_name="Дата рождения", null=False)
    slug = models.SlugField(verbose_name="Слаг", max_length=90, unique=True, null=False)

    # TODO: add achivement system (?)

    def __repr__(self) -> str:
        return f"<CustomUser: {self.username}>"

    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        self.slug = self.username
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"