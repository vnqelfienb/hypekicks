from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView

from .forms import ProfileForm
from .models import Profile


class ProfileDetailView(DetailView):
    template_name = "cotton/profiles/profile.html"
    context_object_name = "profile"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if request.htmx:
            profile = self.get_object()
            form = ProfileForm(instance=profile)
            return render(
                request, self.template_name, {"form": form, "profile": profile}
            )


class ProfileSetupView(FormView):
    template_name = "cotton/profiles/profile_setup.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs["instance"] = getattr(self.request.user, "profile", None)
        return kwargs

    def form_valid(self, form):
        form.save()
        if self.request.htmx:
            response = HttpResponse(status=200)
            response["HX-Redirect"] = self.success_url

            messages.success(
                self.request,
                f"profile updated successfuly",
            )
            return response

        return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(self.request, self.template_name, {"form": form})
        return super().form_invalid(form)


class ProfileUpdateView(FormView):
    template_name = "cotton/profiles/profile_update.html"
    form_class = ProfileForm
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = get_object_or_404(Profile, user=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.save()
        if self.request.htmx:
            response = HttpResponse(status=200)
            response["HX-Redirect"] = self.success_url

            messages.success(
                self.request,
                f"profile updated successfuly",
            )
            return response

        return redirect(self.success_url)

    def form_invalid(self, form):
        if self.request.htmx:
            return render(self.request, self.template_name, {"form": form})
        return super().form_invalid(form)
