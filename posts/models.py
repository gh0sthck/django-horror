from django.db import models
from slugify import slugify

from users.models import CustomUser


class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор комментария")
    comment = models.TextField(verbose_name="Оставьте свой комментарий", null=False)
    answer = models.ManyToManyField("Comments", blank=True) # (?) to comment threads
    # TODO: likes to commnt (redis?)
    date = models.DateTimeField(verbose_name="Дата комменатрия", auto_now_add=True)

    def __repr__(self) -> str:
        return f"<Comment: {self.user.username}: {self.comment[:20]}>"
    
    def __str__(self) -> str:
        return self.comment[:20]

    class Meta:
        ordering = ["pk"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комменатрии"


class Post(models.Model):
    title = models.CharField(max_length=90, verbose_name="Имя поста", unique=True, null=False)
    text = models.TextField(verbose_name="Содержание", null=False)  # temporary - field will updated
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    description = models.TextField(max_length=512, verbose_name="Описание", null=True, blank=True)
    # TODO: views - redis array
    # TODO: likes - redis array
    # TODO: tags - many-to-many in orm
    comments = models.ManyToManyField(Comments, verbose_name="Комментарии", blank=True)
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateField(auto_now_add=True, verbose_name="Дата изменения")
    slug = models.SlugField(verbose_name="Слаг", max_length=90, unique=True, null=False)

    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return f"<Post: {self.title}>"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save()

    def get_comments(self) -> list[Comments]:
        return self.comments.all()
    
    def get_comments_count(self) -> int:
        return len(self.comments.all())

    class Meta:
        ordering = ["-title"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"



