from django.http import HttpRequest
from django.shortcuts import render

from .forms import LoginForm

def index(request: HttpRequest):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            print("Form is valid")

        else:
            print("Invalid form", request.POST)

    return render(request, 'index.html')
