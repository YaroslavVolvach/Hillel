from django.urls import path
from .models import Post

from django.views.generic.list import ListView
from . import views


app_name = 'post'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<str:my_post>/', views.PostListView.as_view(), name='my_posts'),
    path('post_create', views.PostCreateView.as_view(), name='post_create'),
    path('post_update/<int:post_id>/', views.PostUpdateView.as_view(), name='post_update'),
    path('post_detail/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post_delete/<int:post_id>', views.PostDeleteView.as_view(), name='post_delete'),
    ]