from django.urls import path

from .views import Collaborative

urlpatterns = [path("collaborative/", Collaborative.as_view())]
