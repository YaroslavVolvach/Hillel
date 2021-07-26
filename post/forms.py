from django import forms
from .models import Post
from django.forms.widgets import TextInput


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ('title', 'text')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }

    def save(self, user):
        post = super().save(commit=False)
        post.created_by = user
        post.save()
        return post
