from django.urls import path

from .views import CreatePostView, MainPage, PostView

urlpatterns = [
    path("", MainPage.as_view(), name="main"),
    path("create/", CreatePostView.as_view(), name="create_post"),
    path("<slug:slug>/", PostView.as_view(), name="specific_post"),
]
