import os
from urllib.parse import urlencode

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate

from requests import Request

from .forms import LoginForm

def index(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(email=email, password=password)

            if user is not None:
                return redirect(request.GET.get('next'))

    keyrock_url = f'{os.getenv("KEYROCK_URL")}/oauth2/authorize'

    params = {
        'response_type': 'token',
        'client_id': os.getenv("CLIENT_ID"),
        'state': 'xyz',
        'redirect_uri': 'http://localhost:8000/home',
    }

    keyrock = Request("POST", url=keyrock_url, params=urlencode(params, safe='/:')).prepare()


    form = LoginForm()
    return render(request, 'index.html', { 'login_form': form , 'keyrock_url': keyrock.url})
