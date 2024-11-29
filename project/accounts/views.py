from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import FormView

from .forms import LoginForm, SignUpForm


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


class SignUpView(FormView):
    template_name = "signup.html"
    partial_template_name = "cotton/signup_partial.html"
    form_class = SignUpForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        user = form.save()
        logout(self.request)

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
