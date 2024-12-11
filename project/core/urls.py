from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
    path("about/", views.AboutUsPageView.as_view(), name="about"),
]
