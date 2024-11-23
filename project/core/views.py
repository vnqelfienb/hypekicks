from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import LoginForm


class IndexPageView(TemplateView):
    template_name = "index.html"
