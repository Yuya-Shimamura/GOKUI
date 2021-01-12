from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile
from accounts.models import User, FriendShip
from main_app.models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ProfileEditForm

from django.contrib.auth.decorators import login_required

# Follow機能
from django.template.loader import render_to_string
from django.http import JsonResponse

class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser

class ProfileView(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(id=self.kwargs['pk'])

        profile_user = profile.user
        current_user = request.user
        followee_count = current_user.followees.all().count()
        follow_rest = 3 - followee_count
        followees = profile_user.followees.all()
        followees_posts = Post.objects.filter(user__in=followees).order_by('-created_at')[0:6]
        favorite_posts = Post.objects.filter(favorite=profile_user).order_by('-created_at')
        

        if profile_user == current_user:
            follow_status_code = 1
        else:
            follow_status_code = 2

        follow = False
        if profile_user.followers.filter(id=current_user.id).exists():
            follow = True

        return render(request, 'user_profile/profile.html', {
            'profile': profile,
            'follow_status_code': follow_status_code,
            'follow': follow,
            'followees_posts': followees_posts,
            'favorite_posts': favorite_posts,
            'follow_rest': follow_rest,
        })

@login_required
def follow(request):
    current_user = request.user
    profile_user = get_object_or_404(User, id=request.POST.get('profile_user'))
    profile = profile_user.profile
    followee_count = current_user.followees.all().count()
    follow_rest = 3 - followee_count
    followees = profile_user.followees.all()
    followees_posts = Post.objects.filter(user__in=followees).order_by('-id')[0:6]
    favorite_posts = Post.objects.filter(favorite=profile_user).order_by('-created_at')
    

    if profile_user == current_user:
        follow_status_code = 1
    else:
        follow_status_code = 2

    follow = False
    if current_user == profile_user:
        raise PermissionDenied()
    elif profile_user.followers.filter(id=current_user.id).exists():
        # follow_rest += 1
        profile_user.followers.remove(current_user)
        follow = False
    elif current_user not in profile_user.followers.all() and follow_rest != 0:
        # follow_rest -= 1
        profile_user.follower_friendships.create(follower=current_user)
        follow = True
    elif follow_rest == 0:
        pass

    # context = {
    #     'profile': profile,
    #     'follow_status_code': follow_status_code,
    #     'follow': follow,
    #     'followees_posts': followees_posts,
    #     'favorite_posts': favorite_posts,
    #     'follow_rest': follow_rest,
    # }
    # if request.is_ajax():
    #     html = render_to_string('user_profile/follow.html', context, request=request)
    #     return JsonResponse({'form': html})
    
    return redirect('profile', pk=profile_user.id)

class ProfileEditView(LoginRequiredMixin, OnlyYouMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = "user_profile/profile_edit.html"
    
    def get_success_url(self):
        userid=self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': userid})

class FolloweesView(TemplateView):
    def get(self, request, *args, **kwargs):
        profile_user = User.objects.get(id=self.kwargs['pk'])
        followees = profile_user.followees.all()

        return render(request, 'user_profile/followees.html', {
            'profile_user': profile_user,
            'followees': followees,
        })

class FollowersView(TemplateView):
    def get(self, request, *args, **kwargs):
        profile_user = User.objects.get(id=self.kwargs['pk'])
        followers = profile_user.followers.all()

        return render(request, 'user_profile/followers.html', {
            'profile_user': profile_user,
            'followees': followers,
        })

