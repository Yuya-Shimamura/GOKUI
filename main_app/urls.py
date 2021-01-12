from django.urls import path, include
from main_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('views_index', views.ViewsIndexView.as_view(), name='views_index'),
    path('like_index', views.LikeIndexView.as_view(), name='like_index'),
    path('favorite_index', views.FavoriteIndexView.as_view(), name='favorite_index'),
    path('one_week_ago_index', views.OneWeekAgoIndexView.as_view(), name='one_week_ago_index'),
    path('one_month_ago_index', views.OneMonthAgoIndexView.as_view(), name='one_month_ago_index'),
    path('post/detail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_create/', views.PostCreateView.as_view(), name='post_create'),
    path('post_edit/<int:pk>/', views.PostEditView.as_view(), name='post_edit'),
    path('post_delete/<int:pk>/', views.PostDeleteView.as_view(), name='post_delete'),
    path('user_post_list/<int:pk>/', views.UserPostListView.as_view(), name='user_post_list'),
    path('post_search/', views.PostSearchView.as_view(), name='post_search'),
    path('post_tag_list/<str:tag>/', views.PostTagListView.as_view(), name='post_tag_list'),
    path('like/', views.like, name='like'),
    path('favorite/', views.favorite, name='favorite'),
    path('comment/<int:pk>', views.comment_create, name='comment_create'),
    path('reply/<int:pk>', views.reply_create, name='reply_create'),
    path('comment_delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment_delete'),
    # path('reply_delete/<int:pk>', views.ReplyDeleteView.as_view(), name='reply_delete'),
]
