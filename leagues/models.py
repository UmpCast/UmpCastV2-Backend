from django.db import models

# Create your models here.


class League(models.Model):
    title = models.CharField(max_length=10)
