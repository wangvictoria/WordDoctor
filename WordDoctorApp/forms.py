from django import forms
from .models import Anagrams, Wordle, Wordscape

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