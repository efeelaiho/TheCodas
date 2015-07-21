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
from operator import add
from functools import reduce

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

def search(request) :
	form = SearchForm()

	query_string = ''
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		artist_field_list = ['full_name', 'genre', 'origin', 'recommended_album.album_name']
		album_field_list = ['album_name', 'genre', 'album_artist.full_name']
		query_results = []
		query_results += [get_query('and', query_string, ['full_name'])]
		query_results += [get_query('and', query_string, ['genre'])]
		query_results += [get_query('and', query_string, ['origin'])]
		query_results += [get_query('and', query_string, ['recommended_album__album_name'])]
		query_results += [get_query('or', query_string, ['full_name'])]
		query_results += [get_query('or', query_string, ['genre'])]
		query_results += [get_query('or', query_string, ['origin'])]
		query_results += [get_query('or', query_string, ['recommended_album__album_name'])]
		query_results += [get_query('and', query_string, ['album_name'])]
		query_results += [get_query('and', query_string, ['genre'])]
		query_results += [get_query('and', query_string, ['album_artist__full_name'])]
		query_results += [get_query('or', query_string, ['album_name'])]
		query_results += [get_query('or', query_string, ['genre'])]
		query_results += [get_query('or', query_string, ['album_artist__full_name'])]
		
		and_artists = []
		or_artists  = []
		and_artist_fields = []
		or_artist_fields = []
		and_albums = []
		or_albums = []
		or_album_fields = []		
		and_album_fields = []

		for x in range(0, 4) :
			if Artist.objects.filter(query_results[x]) :
				artist = Artist.objects.filter(query_results[x])
				and_artist_fields = artist_field(artist_field_list[x % 4], artist)
				and_artists.append(artist)
		for x in range(4, 8) :
			if Artist.objects.filter(query_results[x]) :
				artist = Artist.objects.filter(query_results[x])
				or_artist_fields = artist_field(artist_field_list[x % 4], artist)
				or_artists.append(artist)
		y = 0		
		for x in range(8, 11) :
			if Album.objects.filter(query_results[x]) :
				album = Album.objects.filter(query_results[x])
				and_album_fields = album_field(album_field_list[y % 3], album)
				and_albums.append(album)
			y += 1
		for x in range(11, 14) :
			if Album.objects.filter(query_results[x]) :
				album = Album.objects.filter(query_results[x])
				or_album_fields = album_field(album_field_list[y % 3], album)
				or_albums.append(album)
			y += 1

		# and_artists = zip(reduce(add, and_artists),and_artist_fields)
		# and_albums = zip(reduce(add, and_albums),and_album_fields)
		# or_artists = zip(reduce(add, or_artists),or_artist_fields)
		# or_albums = zip(reduce(add, or_albums),or_album_fields)

		# if Artist.objects.filter(query_results[0]) or Artist.objects.filter(query_results[4]) :
		# 	artist_fields.append('full_name')
		# if Artist.objects.filter(query_results[1]) or Artist.objects.filter(query_results[5]) :
		# 	artist_fields.append('genre')
		# if Artist.objects.filter(query_results[2]) or Artist.objects.filter(query_results[6]) :
		# 	artist_fields.append('origin')
		# if Artist.objects.filter(query_results[3]) or Artist.objects.filter(query_results[7]) :
		# 	artist_fields.append('recommended_album.album_name')
		# if Album.objects.filter(query_results[8]) or Album.objects.filter(query_results[11]) :
		# 	album_fields.append('album_name')
		# if Album.objects.filter(query_results[9]) or Album.objects.filter(query_results[12]) :
		# 	album_fields.append('genre')
		# if Album.objects.filter(query_results[10]) or Album.objects.filter(query_results[13]) :
		# 	album_fields.append('album_artist.full_name')

		artist_and_query = get_query('and', query_string, ['full_name', 'genre', 'origin', 'recommended_album__album_name'])
		album_and_query = get_query('and', query_string, ['album_name', 'genre', 'album_artist__full_name'])
		artist_or_query = get_query('or', query_string, ['full_name', 'genre', 'origin', 'recommended_album__album_name'])
		album_or_query = get_query('or', query_string, ['album_name', 'genre', 'album_artist__full_name'])
		and_artists = zip(Artist.objects.filter(artist_and_query).order_by('full_name'),and_artist_fields)
		and_albums  = zip(Album.objects.filter(album_and_query).order_by('album_name'),and_album_fields)
		or_artists = zip(Artist.objects.filter(artist_or_query).order_by('full_name'),or_artist_fields)
		or_albums  = zip(Album.objects.filter(album_or_query).order_by('album_name'),or_artist_fields)

		context = {'query_string': query_string, 'and_artist_fields': and_artist_fields, 'or_artist_fields': or_artist_fields, 'and_album_fields': and_album_fields, 'or_album_fields': or_album_fields,'and_artists': and_artists, 'and_albums': and_albums, 'or_artists': or_artists, 'or_albums': or_albums}
		return render_to_response('search.html', context, context_instance=RequestContext(request))								

	# 	context = {'query_string': query_string, 'and_artists': and_artists, 'and_albums': and_albums, 'or_artists': or_artists, 'or_albums': or_albums}
	# else :
	# 	context = {'form': form}
	# return render_to_response('search.html', context, context_instance=RequestContext(request))	

def artist_field(field_name, artist):

	result = []
	#artist = list(artists)
	if field_name == 'full_name':
		result = [item.full_name for item in artist]
	if field_name == 'genre':
		result = [item.genre for item in artist]
	if field_name == 'origin':
		result = [item.origin for item in artist]
	if field_name == 'recommended_album.album_name':
		result = [item.recommended_album.album_name for item in artist]
	return result

def album_field(field_name, album):
	result = ''
	if field_name == 'album_name':
		result = [item.album_name for item in album]
	if field_name == 'genre':
		result = [item.genre for item in album]
	if field_name == 'album_artist.full_name':
		result = [item.album_artist.full_name for item in album]
	return result

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

