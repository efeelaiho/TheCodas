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


def kanyewest(request):
	return render(request, "kanyewest.html", {})

def michael(request):
	return render(request, "michael.html", {})

def encore(request):
	return render(request, "encore.html", {})

def bad(request):
	return render(request, "bad.html", {})

def college(request):
	return render(request, "college_drop_out.html", {})