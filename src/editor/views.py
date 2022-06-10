import logging
import os
from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from fiware.model import CollaborativeOrder
from fiware.production import Production

from .forms import CollaborativeForm

logger = logging.getLogger("django")


class Collaborative(LoginRequiredMixin, View):
    """Class for rendering the index page of the collaborative cell manager"""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.__connector = Production(server_url=os.getenv("OCB_URL"))

    def get(self, request: HttpRequest, *_: Any, **__: Any) -> HttpResponse:
        """Respond to incoming GET requests"""
        delete_id = request.GET.get("delete")

        if delete_id is not None:
            # delete the order with the given id
            logger.info("Deleting order with id %s", delete_id)
            order = CollaborativeOrder()
            order.id = delete_id
            self.__connector.delete_production_order(order=order)

            return redirect(request.path)

        return self._render_page(request)

    def post(self, request: HttpRequest):
        """Respond to incoming POST requests (form submits)"""
        form = CollaborativeForm(request.POST)

        if form.is_valid():
            logger.info("Form is valid")
            success = self.__connector.new_production_order(
                order=CollaborativeOrder(
                    incubator_type=form.cleaned_data["inc_type"],
                    part_type=form.cleaned_data["part_type"],
                    count=form.cleaned_data["production_count"],
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

        objects = self.__connector.load_production_orders(order=CollaborativeOrder)

        context = {
            "collab_form": collaborative_form,
            "object_list": objects,
        }

        return render(request, "collaborative/index.html", context)
