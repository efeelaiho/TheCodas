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

def eminem(request):
	return render(request, "eminem.html",{})

<<<<<<< HEAD
def kanyewest(requet):
=======
def kanyewest(request):
>>>>>>> 857c12fce4e3afcb78a8d306f5fc6c61eb8c64a5
	return render(request, "kanyewest.html", {})

def michael(request):
	return render(request, "michael.html", {})