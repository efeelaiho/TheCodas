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
from volumemax.forms import SearchForm
from volumemax.search import get_query, normalize_query

# Create your views here.

################################################################### 
#
#   MAIN NAVBAR
#
###################################################################

def home(request):
	form = SearchForm()
	return render(request, "home.html",{'form': form})

def about(request):
	form = SearchForm()
	return render(request, "about.html", {'form': form})    

def artists(request):
	artists = Artist.objects.all()
	form = SearchForm()
	context = {"artist_list": artists,'form': form}
	return render_to_response("artists.html", context)

def albums(request):
	albums = Album.objects.all()
	form = SearchForm()
	context = {"albums_list": albums,'form': form}
	return render_to_response("albums.html", context)

def artistdatabase(request):
	artists =  Artist.objects.all()
	form = SearchForm()
	context = {"artist_list": artists,'form': form}
	return render(request, "artist_database.html", context)

def albumdatabase(request):
	albums = Album.objects.all()
	form = SearchForm()
	context = {"albums_list": albums, 'form': form}
	return render(request, "album_database.html", context)	
		
################################################################### 
#
#   DYNAMIC - ARTIST - ALBUM
#
################################################################### 

def artist_view(request, name):
	name = name.replace('_', ' ')
	form = SearchForm()
	artist = Artist.objects.get(full_name = name)
	album  = artist.recommended_album
	context = {"album": album, "artist": artist,'form': form}


	return render_to_response("dynamic_artist.html", context)

def album_view(request, name):
	name = name.replace('_', ' ')
	album  = Album.objects.get(album_name = name)
	form = SearchForm()
	artist = album.album_artist
	context = {"album": album, "artist": artist,'form': form}
	return render_to_response('dynamic_album.html', context)

################################################################### 
#
#   SEARCH
#
################################################################### 

# def search_query(request) :
# 	#if request.method == 'GET':
# 	form = SearchForm()
# 	return render(request, 'search_results.html', {'form': form})

def search(request) :
	form = SearchForm()
	#return render(request, 'search.html', {'form': form})
	#return render(request, "search.html")

	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		artist_query = get_query(query_string, ['full_name', 'genre', 'origin'])
		found_artists = Artist.objects.filter(artist_query).order_by('full_name')
		context = { 'query_string': query_string, 'found_artists': found_artists, 'form': form}
	else :
		context = {'form': form}
	return render_to_response('search.html', context, context_instance=RequestContext(request))	

def search_results(request):
	form = SearchForm()
	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		
		entry_query = get_query(query_string, ['title', 'body',])
		
		found_entries = Album.objects.filter(entry_query).order_by('-pub_date')
		context = { 'query_string': query_string, 'found_entries': found_entries, 'form': form}

	return render_to_response('search/search_results.html',
						  { 'query_string': query_string, 'found_entries': found_entries },
						  context_instance=RequestContext(request))


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

