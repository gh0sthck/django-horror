from django.urls import path

from blog.views import (
    CreateNoteView,
    EditNoteView,
    FeedView,
    NewsView,
    NoteView,
)


urlpatterns = [
    path("", FeedView.as_view(), name="blog"),
    path("<slug:slug>", NoteView.as_view(), name="specific_note"),
    path("create/", CreateNoteView.as_view(), name="create_note"),
    path("edit/<slug:slug>", EditNoteView.as_view(), name="edit_note"),
    path("news/", NewsView.as_view(), name="news"),
    path("delete/<slug:slug>", NewsView.as_view(), name="news"),
]
