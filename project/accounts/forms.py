from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField, ReCaptchaV2Checkbox

from .models import CustomUser

# from django_recaptcha.widgets import


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

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
            }
        )
    )

    def authenticate_user(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(username=email, password=password)

        if user is None:
            self.add_error(None, "invalid email or password")

        return user


class SignUpForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                "placeholder": " ",
                "id": "password",
                "required": "required",
            }
        ),
        label="Password",
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                "placeholder": " ",
                "id": "password_confirm",
                "required": "required",
            }
        ),
        label="Confirm Password",
    )

    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox(
            attrs={
                "data-theme": "light",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "email",
                    "required": "required",
                }
            ),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            raise forms.ValidationError(list(e.messages))
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )
        return user
