from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.views import ProfileFavoritesList, ProfileView, RegisterView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
            "login/", 
            LoginView.as_view(template_name="users/login.html"),
            name="login"
        ),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("<slug:slug>/", ProfileView.as_view(), name="profile"),
    path("favs/<slug:slug>/", ProfileFavoritesList.as_view(), name="favs")
]
