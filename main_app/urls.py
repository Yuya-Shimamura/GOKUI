from django.urls import path, include
from main_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_edit/<int:pk>/', views.PostEditView.as_view(), name='post_edit'),
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('user_post_list/<int:pk>/', views.UserPostListView.as_view(), name='user_post_list'),
    path('post_search/', views.PostSearchView.as_view(), name='post_search'),
    path('post_tag_list/<str:tag>/', views.PostTagListView.as_view(), name='post_tag_list'),
]
