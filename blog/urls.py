from django.urls import path

from blog.views import (
    CreateNoteView,
    DeleteNoteView,
    EditNoteView,
    NewsView,
    NoteView,
)


urlpatterns = [
    
    path("create/", CreateNoteView.as_view(), name="create_note"),
    path("edit/<slug:slug>/", EditNoteView.as_view(), name="edit_note"),
    path("delete/<slug:slug>/", DeleteNoteView.as_view(), name="delete_note"),
    path("", NewsView.as_view(), name="blog"),
    path("<slug:slug>/", NoteView.as_view(), name="specific_note"),
]
