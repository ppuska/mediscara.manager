import logging

from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from django.shortcuts import redirect, render

logger = logging.getLogger("django")


def index(request: HttpRequest):
    """Renders the main index of the logout page"""
    if request.user.is_authenticated:
        logout(request)
        logger.info("User successfully logged out")

        return render(request, "logout/index.html")

    return redirect(settings.LOGIN_URL)
