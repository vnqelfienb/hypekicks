from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
]
