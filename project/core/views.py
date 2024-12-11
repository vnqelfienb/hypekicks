from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class IndexPageView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            if (
                hasattr(user, "verification_status")
                and user.verification_status == "not_verified"
            ):
                messages.warning(
                    request,
                    f"Please go to your email {user.email} and activate your account",
                )

        return render(request, self.template_name, {user: "user"})
