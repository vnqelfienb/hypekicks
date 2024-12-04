from django import forms
from django.core.exceptions import ValidationError

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "address",
            "phone_number",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "username",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "first_name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "last_name",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "address",
                }
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "block py-2.5 px-0 w-full text-lg text-zinc-50 bg-transparent border-0 border-b-2 border-accent appearance-none focus:outline-none focus:ring-0 focus:border-primary peer",
                    "placeholder": " ",
                    "id": "phone_number",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.username:
            self.fields.pop("username")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Profile.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with this username already exists.")
        return username
