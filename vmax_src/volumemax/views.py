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


def artist(request, ar_name):
	context = RequestContext(request)

	x = ar_name.replace('_', ' ')

	artist = Artist.objects.get(full_name = x)
	album_url = (artist.recommended_album.album_name).replace(' ', '_')
	album_img_url = (artist.recommended_album.image_url)


	artist_dic = {
	  "full_name": artist.full_name,
      "origin": artist.origin,
      "popularity": artist.popularity,
      "genre": artist.genre,
      "spotify_artist_uri": artist.spotify_artist_uri,
      "biography": artist.biography,
      "youtube_url_1": artist.youtube_url_1,
      "youtube_url_2": artist.youtube_url_2,
      "recommended_album": artist.recommended_album,
      "image_url": artist.image_url,
      "rec_album_url": album_url
	} 

	return render_to_response('dynamic_artist.html', artist_dic, context)




def album(request, al_name):
	context = RequestContext(request)

	x = al_name.replace('_', ' ')

	album = Album.objects.get(album_name = x)
	artist_url = (album.album_artist.full_name).replace








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

