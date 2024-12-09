from django.urls import path

from .views import LoginView, LogoutView, SignUpView, activate, resend_email

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("send-email/", resend_email, name="send_email"),
    path("activate/<uidb64>/<token>", activate, name="activate"),
]
