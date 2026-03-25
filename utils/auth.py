from typing import Callable

from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin


def authenticate_required(func: Callable):
    def wrapper(*args, **kwargs):
        if args[1].user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return redirect("login")

    return wrapper


class ClassLoginRequired(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().dispatch(request, *args, **kwargs)