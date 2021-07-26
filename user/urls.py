from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'user_app'

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        authentication_form=LoginForm,
        template_name='user/login.html',
        redirect_authenticated_user='/'
    ), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout')
    ]
