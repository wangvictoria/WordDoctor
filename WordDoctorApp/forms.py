from django import forms
from .models import Anagrams

class AnagramsForm(forms.ModelForm):
    class Meta:
        model = Anagrams
        fields = (
            'anagrams_letters',
            )