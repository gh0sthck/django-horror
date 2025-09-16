from django.contrib import admin

from .models import Post, Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["comment", "user"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    prepopulated_fields = {"slug": ("title",)}
