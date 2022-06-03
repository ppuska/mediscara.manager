import logging
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

logger = logging.getLogger('django')

def index(request: HttpRequest):
    token = request.GET.get('token')

    if token is not None:
        logger.info("Got token, authenticating user...")
        user = authenticate(token=token)

        if user is not None:
            login(request ,user)

            logger.info("Authentication successful")
            return HttpResponse("User logged in")

        logger.info("Authentication error")
        return HttpResponse("User not logged in")

    logger.info("No token found at /home/ redirecting to /login/")
    return redirect('/login/')