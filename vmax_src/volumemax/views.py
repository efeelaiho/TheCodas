from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
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
	# artists = Artist.objects.all()
	# #x = al_name.replace('_', ' ')
	# try:
	# 	artist_url = artists['full_name'].replace(' ', '_')
	# 	artists.update({'artist_url': artist_url})
	# except:
	# 	# return handler404(request)
	# 	artists['artist_url'] = 'michael_jackson'
	# 	# artists.update({'artist_url': ""})
	# context = {"artist_list": artists}

	#return render_to_response("artists.html", context)
	return render(request, "artists.html", {})  

def albums(request):
	albums = Album.objects.all()
	context = {"albums_list": albums}
	# serializer = AlbumSerializer(albums, many=True)
	# album_dict = JSONRenderer().render(serializer.data)
	#return render_to_response("albums.html", context)
	return render(request, "albums.html", {})


def database(request):
	return render(request, "database.html", {})

		
################################################################### 
#
#   DYNAMIC - ARTIST - ALBUM
#
################################################################### 


def artist(request, ar_name):
	context = RequestContext(request)

	x = ar_name.replace('_', ' ')

	artist = Artist.objects.get(full_name = x)
	album_url = (artist.recommended_album.album_name).replace(' ', '_')
	album_img_url = (artist.recommended_album.image_url)
	serializer = ArtistSerializer(artist, many=True)
	artist_dic = JSONRenderer().render(serializer.data)

	# artist_dic = {
	#   "full_name": artist.full_name,
	#   "origin": artist.origin,
	#   "popularity": artist.popularity,
	#   "genre": artist.genre,
	#   "spotify_artist_uri": artist.spotify_artist_uri,
	#   "biography": artist.biography,
	#   "youtube_url_1": artist.youtube_url_1,
	#   "youtube_url_2": artist.youtube_url_2,
	#   "recommended_album": artist.recommended_album,
	#   "image_url": artist.image_url,
	#   "rec_album_url": album_url
	# } 

	return render_to_response('dynamic_artist.html', artist_dic, context)

def album(request, al_name):
	context = RequestContext(request)

	x = al_name.replace('_', ' ')

	album = Album.objects.get(album_name = x)
	artist_url = (album.album_artist.full_name).replace(' ', '_')
	serializer = AlbumSerializer(artists, many=True)
	album_dict = JSONRenderer().render(serializer.data)

	# album_dic = {
	# 	"album_artist" = album.album_artist,
	# 	"album_name" = album.album_name,
	# 	"release_date" = album.release_date,
	# 	"genre" = album.genre,
	# 	"spotify_albums_uri" = album.spotify_albums_uri,
	# 	"editors_notes" = album.editors_notes,
	# 	"image_url" = album.image_url,
	# 	"artist_url" = artist_url
	# }

	return render_to_response('dynamic_album.html', album_dic, context)





################################################################### 
#
#   ARTISTS
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
#   ALBUMS
#
################################################################### 


def encore(request):
	return render(request, "album/encore.html", {})

def bad(request):
	return render(request, "album/bad.html", {})

def college(request):
	return render(request, "album/college_drop_out.html", {})

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

@csrf_exempt
def artist_list(request):
	"""
	List all artists, or create a new artist.
	"""
	if request.method == 'GET':
		artists = Artist.objects.all()
		serializer = ArtistSerializer(artists, many=True)
		return JSONResponse(serializer.data)

@csrf_exempt
def album_list(request):
	"""
	List all albums, or create a new album.
	"""
	if request.method == 'GET':
		albums = Album.objects.all()
		serializer = AlbumSerializer(albums, many=True)
		return JSONResponse(serializer.data)

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

