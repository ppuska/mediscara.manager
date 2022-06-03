import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .fiware.model import Container
from .fiware.production import Production


class Collaborative(View, LoginRequiredMixin):
    """Class for rendering the index page of the collaborative cell manager"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__connector = Production(server_url=os.getenv("OCB_URL"))

    def get(self, request: HttpRequest):

        print(self.__connector.load_production_orders(Container.get_collaborative_id()))

        return render(request, "collaborative/index.html")
