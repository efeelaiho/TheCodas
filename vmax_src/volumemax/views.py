from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from volumemax.models import *
from django.http import HttpResponse
import json

# Create your views here.

###################################################################	
#
#	MAIN NAVBAR
#
###################################################################

def home(request):
	return render(request, "home.html",{})

def about(request):
	return render(request, "about.html", {})	

def artists(request):
	return render(request, "artists.html", {})	

def albums(request):
	return render(request, "albums.html", {})	


###################################################################	
#
#	DYNAMIC - ARTIST - ALBUM
#
###################################################################	


def artist(request, a_name):
	context = RequestContext(request)

	x = a_name.replace('_', ' ')

	artist = Artist.objects.get(full_name = x)
	album_url = (player.recommended_album).replace(' ', '_')


	player_dic 


def album()






###################################################################	
#
#	ARTISTS
#
###################################################################	


def eminem(request):
	return render(request, "artist/eminem.html",{})


def kanyewest(request):
	return render(request, "artist/kanyewest.html", {})

def michael(request):
	return render(request, "artist/michael.html", {})



###################################################################	
#
#	ALBUMS
#
###################################################################	


def encore(request):
	return render(request, "album/encore.html", {})

def bad(request):
	return render(request, "album/bad.html", {})

def college(request):
	return render(request, "album/college_drop_out.html", {})

