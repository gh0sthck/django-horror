from django.contrib import admin

from blog.models import BlogNote


@admin.register(BlogNote)
class BlogNoteAdmin(admin.ModelAdmin):
    list_display = ["title", "text", "author"]
    prepopulated_fields = {"slug": ("title", )}