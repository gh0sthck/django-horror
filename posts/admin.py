from django.contrib import admin

from .models import Category, Post, Comments


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ["comment", "user"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_date"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]