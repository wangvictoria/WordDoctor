from django.db import models

# Create your models here.

class Anagrams(models.Model):
    anagrams_letters = models.CharField(max_length=10)

class Wordscape(models.Model):
    wordscape_letters = models.CharField(max_length=10)
    wordscape_length = models.IntegerField(blank=True, null=True)

class Wordle(models.Model):
    wordle_loc1 = models.CharField(max_length=1, blank=True, null=True)
    wordle_loc2 = models.CharField(max_length=1, blank=True, null=True)
    wordle_loc3 = models.CharField(max_length=1, blank=True, null=True)
    wordle_loc4 = models.CharField(max_length=1, blank=True, null=True)
    wordle_loc5 = models.CharField(max_length=1, blank=True, null=True)
    wordle_known_letters = models.CharField(max_length=5, blank=True, null=True)
    wordle_invalid_letters = models.CharField(max_length=26, blank=True, null=True)