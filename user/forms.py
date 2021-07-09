from django import forms
from django.forms.widgets import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

attrs_ = {'class': 'form-control'}


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs=attrs_))
    password = forms.CharField(widget=PasswordInput(attrs=attrs_))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_
