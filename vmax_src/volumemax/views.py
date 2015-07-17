from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from volumemax.models import Artist, Album
from volumemax.serializer import ArtistSerializer, AlbumSerializer

# Create your views here.

################################################################### 
#
#   MAIN NAVBAR
#
###################################################################

def home(request):
	return render(request, "home.html",{})

def about(request):
	return render(request, "about.html", {})    

def artists(request):
	artists = Artist.objects.all()
	context = {"artist_list": artists}
	return render_to_response("artists.html", context)

def albums(request):
	albums = Album.objects.all()
	context = {"albums_list": albums}
	return render_to_response("albums.html", context)

def database(request):
	return render(request, "database.html", {})
		
################################################################### 
#
#   DYNAMIC - ARTIST - ALBUM
#
################################################################### 

def artist_view(request, name):
	name = name.replace('_', ' ')

	artist = Artist.objects.get(full_name = name)
	album  = artist.recommended_album
	context = {"album": album, "artist": artist}


	return render_to_response("dynamic_artist.html", context)

def album_view(request, name):
	name = name.replace('_', ' ')
	album  = Album.objects.get(album_name = name)

	artist = album.album_artist
	context = {"album": album, "artist": artist}
	return render_to_response('dynamic_album.html', context)

################################################################### 
#
#   ARTISTS
#
################################################################### 


# def eminem(request):
# 	return render(request, "artist/eminem.html",{})


# def kanyewest(request):
# 	return render(request, "artist/kanyewest.html", {})

# def michael(request):
# 	return render(request, "artist/michael.html", {})



################################################################### 
#
#   ALBUMS
#
################################################################### 


# def encore(request):
# 	return render(request, "album/encore.html", {})

# def bad(request):
# 	return render(request, "album/bad.html", {})

# def college(request):
# 	return render(request, "album/college_drop_out.html", {})

################################################################### 
#
#   API
#
###################################################################

class JSONResponse(HttpResponse):
	"""
	An HttpResponse that renders its content into JSON.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@api_view()
def artist_list(request):
	"""
	List all artists, or create a new artist.
	"""
	if request.method == 'GET':
		artists = Artist.objects.all()
		serializer = ArtistSerializer(artists, many=True)
		return JSONResponse(serializer.data)

@api_view()
def album_list(request):
	"""
	List all albums, or create a new album.
	"""
	if request.method == 'GET':
		albums = Album.objects.all()
		serializer = AlbumSerializer(albums, many=True)
		return JSONResponse(serializer.data)

@api_view()
def artist_detail(request, pk):
	"""
	Retrieve an artist.
	"""
	try:
		artist = Artist.objects.get(pk=pk)
	except Artist.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = ArtistSerializer(artist)
		return JSONResponse(serializer.data)

@api_view()
def album_detail(request, pk):
	"""
	Retrieve an album.
	"""
	try:
		album = Album.objects.get(pk=pk)
	except Album.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = AlbumSerializer(album)
		return JSONResponse(serializer.data)

