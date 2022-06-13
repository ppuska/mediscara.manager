from django.urls import path

from .views import Collaborative, Industrial

urlpatterns = [
    path("collaborative/", Collaborative.as_view()),
    path("industrial/", Industrial.as_view()),
]
