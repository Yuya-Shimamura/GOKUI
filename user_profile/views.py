from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProfileEditForm

class ProfileView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs['pk'])

        return render(request, 'user_profile/profile.html', {
            'profile': profile,
        })

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "user_profile/profile_edit.html"
    
    def get_success_url(self):
        userid=self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': userid})
