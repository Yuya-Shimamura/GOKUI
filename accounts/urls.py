from django.urls import path, include
from accounts import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
