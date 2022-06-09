import logging
import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from .fiware.model import CollaborativeOrder, Container
from .fiware.production import Production
from .forms import CollaborativeForm
from .models import CollaborativeModel

logger = logging.getLogger("django")


class Collaborative(LoginRequiredMixin, View):
    """Class for rendering the index page of the collaborative cell manager"""

    model = CollaborativeModel

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__connector = Production(server_url=os.getenv("OCB_URL"))

    def get(self, request: HttpRequest, *_: Any, **__: Any) -> HttpResponse:
        """Respond to incoming GET requests"""
        delete_order = request.GET.get("delete")

        if delete_order is not None:
            # delete the order with the given creation date
            logger.info("Deleting order with creation date %s", delete_order)
            self.__connector.delete_production_order(
                container_id=Container.get_collaborative_id(), created=delete_order
            )

            return redirect(request.path)

        return self._render_page(request)

    def post(self, request: HttpRequest):
        """Respond to incoming POST requests (form submits)"""
        form = CollaborativeForm(request.POST)

        if form.is_valid():
            logger.info("Form is valid")
            success = self.__connector.new_production_order(
                order=CollaborativeOrder(
                    incubator_type=form.cleaned_data["inc_type"], count=form.cleaned_data["production_count"]
                )
            )

            if success:
                logger.info("Order successfully added")

            else:
                logger.warning("Could not add new production order")

            return redirect(request.path)

        logger.info("Form is invalid")

        return self._render_page(request)

    def _render_page(self, request: HttpRequest):
        """Renders the page contents"""
        collaborative_form = CollaborativeForm()

        objects = []
        container = self.__connector.load_production_orders(Container.get_collaborative_id())

        for entity in container.order_list:
            objects.append(CollaborativeModel.create_from_dataclass(entity))

        context = {
            "collab_form": collaborative_form,
            "object_list": objects,
        }

        return render(request, "collaborative/index.html", context)
