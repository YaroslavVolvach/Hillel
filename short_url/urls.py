from django.urls import path

from . import views

app_name = 'short_url'

urlpatterns = [
    path('', views.url_generator, name='url_generator'),
    path('url_redirect/', views.url_redirect, name='url_redirect'),
    path('url_redirect/<str:short_url>/', views.url_redirect, name='url_redirect_initial')
]


