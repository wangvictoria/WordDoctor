from django.db import models

# Create your models here.

class Anagrams(models.Model):
    anagrams_letters = models.CharField(max_length=10)