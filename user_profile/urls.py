from django.urls import path, include
from user_profile import views

urlpatterns = [
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("profile_edit/<int:pk>", views.ProfileEditView.as_view(), name="profile_edit"),
]
