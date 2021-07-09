from django import forms
from django.forms.widgets import URLInput, TextInput
from django.shortcuts import get_object_or_404
from urllib.parse import urlparse
from .models import ShortURL
from random import choice
from string import ascii_letters, digits

# first_name = forms.URLField(widget=forms.URLField())

access = ('http', 'https', 'ftp')


class URLForm(forms.Form):
    url = forms.URLField(widget=URLInput(attrs={'class': 'form-control'}))

    def __init__ (self, *args, **kwargs):
        self.short_url = 'short/{}'.format(
            ''.join(choice(ascii_letters + digits) for i in range(7))
        )
        super().__init__(*args, **kwargs)

    def is_valid(self):
        if super().is_valid():
            if urlparse(self.cleaned_data['url']).scheme in access:
                return True

        return False

    def save(self):
        if ShortURL.objects.filter(url=self.cleaned_data['url']):
            instance = get_object_or_404(
                ShortURL, url=self.cleaned_data['url']
            )

        else:
            instance = ShortURL.objects.create(
                url=self.cleaned_data['url'],
                short_url=self.short_url
            )
        return instance


class URLRedirectForm(forms.Form):
    short_url = forms.CharField(
        widget=TextInput(attrs={'class': 'form-control'}))

    def save(self):
        instance = get_object_or_404(ShortURL,
                                     short_url=self.cleaned_data['short_url'])
        instance.redirect_count += 1
        instance.save()

        return instance
