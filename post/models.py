from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField()
    slug = models.SlugField(max_length=70, unique=True)
    created_by = models.ForeignKey(User,  on_delete=models.CASCADE,
                                   related_name='post')
    created_at = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.id])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify('{}_{}'.format(self.created_by, self.title))
        super().save(*args, **kwargs)


