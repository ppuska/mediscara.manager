import logging

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from django.shortcuts import redirect, render

logger = logging.getLogger("django")


def index(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "home/index.html")

    token = request.GET.get("token")

    if token is not None:
        logger.info("Got token, authenticating user...")
        user = authenticate(token=token)

        if user is not None:
            login(request, user)

            logger.info("Authentication successful")
            return render(request, "home/index.html")

        logger.info("Authentication error")
        return redirect(settings.LOGIN_URL)

    logger.info("No token found at /home/ redirecting to /login/")
    return redirect(settings.LOGIN_URL)
