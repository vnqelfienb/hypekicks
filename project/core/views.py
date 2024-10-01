from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm


def index(request):
    return render(request, "index.html")


def login(request):

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            if user:
                auth_login(request, user)
                if request.htmx:
                    return HttpResponse(status=204)
                return redirect("index")
        if request.htmx:
            return render(request, "cotton/login_partial.html", {"form": form})
    else:
        form = LoginForm()

    if request.htmx:
        return render(request, "login.html", {"form": form})
    else:
        return redirect("index")
