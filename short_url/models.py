from django.db import models


class ShortURL(models.Model):
    url = models.URLField(unique=True)
    short_url = models.URLField(unique=True)
    redirect_count = models.PositiveSmallIntegerField(default=0)
