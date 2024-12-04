from django.urls import path

from .views import ProfileDetailView, ProfileSetupView, ProfileUpdateView

urlpatterns = [
    path("details/", ProfileDetailView.as_view(), name="profile_details"),
    path("setup/", ProfileSetupView.as_view(), name="profile_setup"),
    path("update/", ProfileUpdateView.as_view(), name="profile_update"),
]
