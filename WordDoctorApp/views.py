from django.shortcuts import render

# Create your views here.

def index(request):
    """View function for home page of site."""

    context = {}

    return render(request, 'index.html', context)

def wordle(request):
    context = {}
    return render(request, 'wordle.html', context)

def scrabble(request):
    context = {}
    return render(request, 'scrabble.html', context)

def anagrams(request):
    context = {}
    return render(request, 'anagrams.html', context)

def boggle(request):
    context = {}
    return render(request, 'boggle.html', context)

def wordscape(request):
    context = {}
    return render(request, 'wordscape.html', context)

def general(request):
    context = {}
    return render(request, 'general.html', context)