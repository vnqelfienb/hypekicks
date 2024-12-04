from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the currently logged-in user

        if user.is_authenticated:  # Ensure the user is logged in
            # Check if the user has a verification_status attribute and if it's 'not_verified'
            if (
                hasattr(user, "verification_status")
                and user.verification_status == "not_verified"
            ):
                messages.warning(
                    request,
                    f"Please go to your email {user.email} and activate your account",
                )

        return render(request, self.template_name, {user: "user"})
