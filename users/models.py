from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=90, verbose_name="Имя пользователя", unique=True, null=False)
    bio = models.TextField(verbose_name="О себе", max_length=256, blank=True, default="")
    email = models.EmailField(verbose_name="Электронная почта", unique=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    birthday = models.DateField(verbose_name="Дата рождения", null=True)
    slug = models.SlugField(verbose_name="Слаг", max_length=90, unique=True, null=False)
    
    favorites = models.ManyToManyField("posts.Post", verbose_name="Избранное", blank=True)
    blog_following = models.ManyToManyField("CustomUser", verbose_name="Подписки", blank=True)

    # TODO: add achivement system (?)

    def __repr__(self) -> str:
        return f"<CustomUser: {self.username}>"

    def __str__(self) -> str:
        return self.username
    
    def save(self, *args, **kwargs):
        self.slug = self.username
        return super().save(*args, **kwargs)
    
    def add_to_favorites(self, post):
        self.favorites.add(post)
        self.save()
        
    def remove_from_favorites(self, post):
        self.favorites.remove(post)
        self.save()
        
    def follow_user(self, user):
        self.blog_following.add(user)
        self.save()
        
    def unfollow_user(self, user):
        self.blog_following.remove(user)
        self.save()

    class Meta:
        ordering = ["-username"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
