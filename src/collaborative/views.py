from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class Index(View, LoginRequiredMixin):
    """Class for rendering the index page of the collaborative cell manager"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get(self, request: HttpRequest):
        pass


@login_required
def index(request: HttpRequest):
    return render(request, "collaborative/index.html")
