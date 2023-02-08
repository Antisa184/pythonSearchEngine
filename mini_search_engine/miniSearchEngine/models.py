from django.db import models

# Create your models here.

class TextRecord(models.Model):
    record = models.CharField(max_length=255)