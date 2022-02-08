from django import forms
from .models import Anagrams, Wordscape

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