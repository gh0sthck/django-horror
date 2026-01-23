from django.db import models
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field

from users.models import CustomUser


class BlogNote(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=90)
    slug = models.SlugField(verbose_name="Слаг", max_length=90)
    # text = models.TextField(verbose_name="Текст", null=False)
    text = CKEditor5Field("Содержание")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    is_news = models.BooleanField(verbose_name="Новость", default=False)
    pubdate = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата изменений")
    # TODO: tags
    # TODO: likes
    # TODO: view
    cover = models.ImageField(verbose_name="Обложка", upload_to="news", null=True, blank=True)

    def __repr__(self) -> str:
        return f"<BlogNote: {self.title}>"
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        ordering = ["-title"]
