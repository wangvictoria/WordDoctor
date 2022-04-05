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
    wordle_loc6 = models.CharField(max_length=5, blank=True, null=True)
    wordle_loc7 = models.CharField(max_length=5, blank=True, null=True)
    wordle_loc8 = models.CharField(max_length=5, blank=True, null=True)
    wordle_loc9 = models.CharField(max_length=5, blank=True, null=True)
    wordle_loc10 = models.CharField(max_length=5, blank=True, null=True)
    wordle_known_letters = models.CharField(max_length=5, blank=True, null=True)
    wordle_invalid_letters = models.CharField(max_length=26, blank=True, null=True)

class Boggle(models.Model):
    boggle_11 = models.CharField(max_length=1)
    boggle_12 = models.CharField(max_length=1)
    boggle_13 = models.CharField(max_length=1)
    boggle_14 = models.CharField(max_length=1)

    boggle_21 = models.CharField(max_length=1)
    boggle_22 = models.CharField(max_length=1)
    boggle_23 = models.CharField(max_length=1)
    boggle_24 = models.CharField(max_length=1)

    boggle_31 = models.CharField(max_length=1)
    boggle_32 = models.CharField(max_length=1)
    boggle_33 = models.CharField(max_length=1)
    boggle_34 = models.CharField(max_length=1)

    boggle_41 = models.CharField(max_length=1)
    boggle_42 = models.CharField(max_length=1)
    boggle_43 = models.CharField(max_length=1)
    boggle_44 = models.CharField(max_length=1)

class Scrabble(models.Model):
    scrabble_letters = models.CharField(max_length=10)
    scrabble_open = models.CharField(max_length=10)