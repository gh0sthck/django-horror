from django.urls import path

from .views import CreatePostView, DeletePostView, MainPage, PostView, UpdatePostView

urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("update/<slug:slug>/", UpdatePostView.as_view(), name="update_post"),
    path("delete/<slug:slug>/", DeletePostView.as_view(), name="delete_post"),
    path("<slug:slug>/", PostView.as_view(), name="specific_post"),
]
