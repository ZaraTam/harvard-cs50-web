from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random"),
    path("<str:title>", views.entry, name="entry")
]
