from django.db import models

# Create your models here.


class Song(models.Model):
    slug = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    body = models.TextField()
