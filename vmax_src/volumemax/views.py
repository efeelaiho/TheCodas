from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from volumemax.models import Artist, Album
from volumemax.serializer import ArtistSerializer, AlbumSerializer

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

###################################################################	
#
#	API
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