from django.shortcuts import render, redirect, get_object_or_404
from .forms import URLForm, URLRedirectForm
from .models import ShortURL


def url_generator(request):
    if not request.user.is_authenticated:
        return redirect('short_url:url_redirect')

    context = dict(form=URLForm())
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            return redirect('short_url:url_redirect_initial', form.short_url)

        context['error'] = 'URL must start with "https", "http" or "ftp" '
    return render(request, 'short_url/url_generator.html', context)


def url_redirect(request, short_url=None):
    if request.method == 'POST':
        form = URLRedirectForm(request.POST)
        if form.is_valid():
            instance = form.save()
            return redirect(instance.url)

    form = URLRedirectForm()
    if short_url is not None:
        form = URLRedirectForm(initial={'short_url': short_url})
    return render(request, 'short_url/url_redirect.html', {'form': form})
