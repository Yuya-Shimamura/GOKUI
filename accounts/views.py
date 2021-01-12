from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import SignUpForm
from allauth.account import views
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"


class LogoutView(views.LogoutView):
    template_name = "registration/logout.html"

    # def post(self, request, *args, **kwargs):
    #     if self.request.user.is_authenticated:
    #         self.request.user.logout()
    #     return redirect('/')