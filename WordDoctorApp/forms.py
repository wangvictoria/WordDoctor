from django import forms
from .models import Anagrams, Boggle, Wordle, Wordscape

class AnagramsForm(forms.ModelForm):
    class Meta:
        model = Anagrams
        fields = (
            'anagrams_letters',
            )

class WordscapeForm(forms.ModelForm):
    class Meta:
        model = Wordscape
        fields = (
            'wordscape_letters',
            'wordscape_length',
        )

class WordleForm(forms.ModelForm):
    class Meta:
        model = Wordle
        fields = (
            'wordle_loc1',
            'wordle_loc2',
            'wordle_loc3',
            'wordle_loc4',
            'wordle_loc5',
            'wordle_known_letters',
            'wordle_invalid_letters',
        )
    
    # TODO: include error checking so that letters in wordle_invalid_letters are not in the other inputs

class BoggleForm(forms.ModelForm):
    class Meta:
        model = Boggle
        fields = (
            'boggle_11',
            'boggle_12',
            'boggle_13',
            'boggle_14',
            'boggle_21',
            'boggle_22',
            'boggle_23',
            'boggle_24',
            'boggle_31',
            'boggle_32',
            'boggle_33',
            'boggle_34',
            'boggle_41',
            'boggle_42',
            'boggle_43',
            'boggle_44',
        )