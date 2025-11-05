from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import ProfileEditView, ProfileFavoritesList, ProfileFollowersView, ProfileStoriesView, ProfileSubscribesView, ProfileView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
            "login/", 
            LoginView.as_view(template_name="users/login.html"),
            name="login"
        ),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("<slug:slug>/", ProfileView.as_view(), name="profile"),
    path("favs/<slug:slug>/", ProfileFavoritesList.as_view(), name="favs"),
    path("subs/<slug:slug>/", ProfileSubscribesView.as_view(), name="subs"),
    path("followers/<slug:slug>/", ProfileFollowersView.as_view(), name="follows"),
    path("stories/<slug:slug>/", ProfileStoriesView.as_view(), name="us_stories"),
    path("edit/<slug:slug>/", ProfileEditView.as_view(), name="us_update"),
]
