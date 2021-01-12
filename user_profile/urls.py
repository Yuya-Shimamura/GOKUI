from django.urls import path, include
from user_profile import views

urlpatterns = [
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("profile_edit/<int:pk>", views.ProfileEditView.as_view(), name="profile_edit"),
    path("follow/", views.follow, name="follow"),
    path("followees_list/<int:pk>", views.FolloweesView.as_view(), name="followees_list"),
    path("followers_list/<int:pk>", views.FollowersView.as_view(), name="followers_list"),
]
