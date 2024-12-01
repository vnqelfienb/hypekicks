from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import View
from django.views.generic.edit import FormView

from .forms import LoginForm, SignUpForm
from .tokens import account_activation_token


class LoginView(FormView):
    template_name = "login.html"
    partial_template_name = "cotton/login_partial.html"
    form_class = LoginForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.authenticate_user()
        if user:
            auth_login(self.request, user)

            if self.request.htmx:
                response = HttpResponse(status=200)
                response["HX-Redirect"] = self.success_url
                return response
            return redirect(self.success_url)
        return self.form_invalid(form)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(self.request, self.partial_template_name, {"form": form})
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            form = self.get_form(self.form_class)
            return render(request, self.template_name, {"form": form})
        return redirect(self.success_url)


class LogoutView(View):
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        if request.htmx:
            response = HttpResponse(status=200)
            response["HX-Redirect"] = self.success_url
            logout(request)
            return response
        return redirect(self.success_url)


def activate_email(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "cotton/activate_account.html",
        {
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(
            request,
            f"an activation link was sent to {to_email}",
        )
    else:
        messages.error(
            request,
            f"problem sending confirmation email to {to_email}, check if you typed it correctly.",
        )


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.verification_status = "verified"
        user.save()

        messages.success(
            request,
            "thank you for your email confirmation.",
        )
        return redirect("index")
    else:
        messages.error(request, "activation link is invalid!")

    return redirect("index")


class SignUpView(FormView):
    template_name = "signup.html"
    partial_template_name = "cotton/signup_partial.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        activate_email(self.request, user, form.cleaned_data.get("email"))
        auth_login(self.request, user)

        if self.request.htmx:
            response = HttpResponse(status=200)
            response["HX-Redirect"] = self.success_url
            return response

        return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(self.request, self.partial_template_name, {"form": form})
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            form = self.get_form(self.form_class)
            return render(request, self.template_name, {"form": form})
        return redirect(self.success_url)
