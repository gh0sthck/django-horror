from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import (
    ProfileDeleteView,
    ProfileEditView,
    ProfileFavoritesList,
    ProfileFollowersView,
    ProfileStoriesView,
    ProfileSubscribesView,
    ProfileView,
    RegisterView,
    CustomLoginView,
    change_password_view,
    email_verification_view
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("<slug:slug>/", ProfileView.as_view(), name="profile"),
    path("favs/<slug:slug>/", ProfileFavoritesList.as_view(), name="favs"),
    path("subs/<slug:slug>/", ProfileSubscribesView.as_view(), name="subs"),
    path("followers/<slug:slug>/", ProfileFollowersView.as_view(), name="follows"),
    path("stories/<slug:slug>/", ProfileStoriesView.as_view(), name="us_stories"),
    path("edit/<slug:slug>/", ProfileEditView.as_view(), name="us_update"),
    path("delete/<slug:slug>/", ProfileDeleteView.as_view(), name="us_delete"),
    path("email_verification", email_verification_view, name="verify_email"),
    path("password_change", change_password_view, name="change_password")
]
