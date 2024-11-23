from django import forms
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                "placeholder": " ",
                "id": "email",
                "required": "required",
            }
        ),
        label="email",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                "placeholder": " ",
                "id": "password",
                "required": "required",
            }
        ),
        label="password",
    )

    def authenticate_user(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)

        if user is None:
            self.add_error(None, "invalid email or password")

        return user
