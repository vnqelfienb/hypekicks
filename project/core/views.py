from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")

def login(reqest):
    return render(reqest, "login.html")
