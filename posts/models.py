from dataclasses import dataclass
from typing import Optional
from django.db import models
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field

from users.models import CustomUser

@dataclass
class CommentModel:
    comment: str
    answer: Optional["CommentModel"] = None

class Comments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор комментария")
    comment = models.TextField(verbose_name="", null=False)
    answer = models.ManyToManyField("Comments", blank=True) # (?) to comment threads
    # TODO: likes to commnt (redis?)
    date = models.DateTimeField(verbose_name="Дата комменатрия", auto_now_add=True)

    def get_comms(self, index: int = 1, comment: "Comments" = None, ls: list = []):
        if not comment:
            comment = self
        ls.append((index, comment))
        for answer in comment.answer.all():
            if answer.answer.all():
                ls.append(Post.get_comms(index=index+1, comment=answer.answer, ls=ls))
                # return ls
        print(ls)
        return ls

    # def get_answers(self, ls=None, result:list=[]):
    #     if not ls:
    #         ls = Comments.objects.filter(answer=self)
    #     for comment in ls:
    #         answers_to_comment = Comments.objects.filter(answer=comment)
    #         print("curr commnt", comment)
    #         if len(answers_to_comment) == 0:
    #             print("comment lst", comment)
    #             return 
    #         else:
    #             self.get_answers(answers_to_comment)
    #         return result

    def __repr__(self) -> str:
        return f"<Comment: {self.user.username}: {self.comment[:20]}>"
    
    def __str__(self) -> str:
        return self.comment[:20]

    class Meta:
        ordering = ["pk"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комменатрии"


class Category(models.Model):
    name = models.CharField(max_length=90, verbose_name="Имя категории", unique=True, null=False)
    
    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return f"<Category: {self.name}>"
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["-name"]


class Tag(models.Model):
    name = models.CharField(verbose_name="Имя тега", max_length=80, null=False)
    
    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag: {self.name}>"
    
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["-name"]


class Post(models.Model):
    title = models.CharField(max_length=90, verbose_name="Имя поста", unique=True, null=False)
    text = CKEditor5Field("Содержание")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Автор")
    description = models.TextField(max_length=512, verbose_name="Описание", null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", blank=True)
    # TODO: views - redis array
    # TODO: likes - redis array
    comments = models.ManyToManyField(Comments, verbose_name="Комментарии", blank=True)
    created_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateField(auto_now_add=True, verbose_name="Дата изменения")
    slug = models.SlugField(verbose_name="Слаг", max_length=90, unique=True, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    cover = models.ImageField(verbose_name="Обложка", null=True, blank=True, upload_to="posts")

    def __str__(self) -> str:
        return self.title
    
    def __repr__(self) -> str:
        return f"<Post: {self.title}>"
   
    def get_cover(self):
        try:  
            cover = self.cover.url
        except ValueError:
            cover = "/static/defaults/avatar.png"
        return cover
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_comments(self) -> list[Comments]:
        return self.comments.all()
    
    def get_comments_count(self) -> int:
        return len(self.comments.all())

    class Meta:
        ordering = ["-title"]
        verbose_name = "Пост"
        verbose_name_plural = "Посты"



