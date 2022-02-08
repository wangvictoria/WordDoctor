from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('wordle/', views.wordle, name='wordle'),
    path('scrabble/', views.scrabble, name='scrabble'),
    path('anagrams/', views.anagrams, name='anagrams'),
    path('boggle/', views.boggle, name='boggle'),
    path('wordscapes/', views.wordscape, name='wordscape'),
]