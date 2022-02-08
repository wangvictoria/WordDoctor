from django.db import models

# Create your models here.

class Anagrams(models.Model):
    anagrams_letters = models.CharField(max_length=10)

class Wordscape(models.Model):
    wordscape_letters = models.CharField(max_length=10)
    wordscape_length = models.IntegerField(blank=True, null=True)