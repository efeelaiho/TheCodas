from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, "home.html",{})

def about(request):
	return render(request, "about.html", {})	

def artists(request):
	return render(request, "artists.html", {})	

def albums(request):
	return render(request, "albums.html", {})	