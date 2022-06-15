import os
from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View
from requests import Request

from .forms import LoginForm


class Index(View):
    """Main index page of the Login screen"""

    def get(self, request: HttpRequest):
        """Respond to GET requests"""
        # process logout request
        if request.GET.get("logged_out") is not None:
            logout(request)
            return self._render_page(request, login_failed=False, logged_out=True)

        # check if the user is signed in
        if request.user.is_authenticated:
            return redirect("/home/")  # redirect back to homepage

        return self._render_page(request, login_failed=False, logged_out=False)

    def post(self, request: HttpRequest):
        """Respond to POST requests"""
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                redirect_to = request.GET.get("next")

                if redirect_to is None:
                    redirect_to = "/home/"

                return redirect(redirect_to)

        return self._render_page(request, login_failed=True, logged_out=False)

    def _render_page(self, request: HttpRequest, login_failed: bool, logged_out: bool):
        """Renders the page

        Args:
            login_failed (bool): if the user has failed the login form
            logged_out (bool): if the user has completed the logout process
        """
        # create context for keyrock auth request
        keyrock_url = f'{os.getenv("KEYROCK_URL")}/oauth2/authorize'
        server_ip = os.getenv("HOST_IP")

        params = {
            "response_type": "token",
            "client_id": os.getenv("CLIENT_ID"),
            "state": "xyz",
            "redirect_uri": f"{server_ip}:8000/home",
        }

        keyrock = Request("POST", url=keyrock_url, params=urlencode(params, safe="/:")).prepare()

        # create context for the login form
        form = LoginForm()

        # create context
        context = {
            "login_form": form,
            "keyrock_url": keyrock.url,
            "grafana_url": f"{server_ip}:3000",
            "login_failed": login_failed,
            "logged_out": logged_out,
        }

        return render(request, "login/index.html", context)
