from django.forms import widgets
from rest_framework import serializers
from volumemax.models import Artist, Album

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('full_name', 'origin', 'popularity', 'genre', 'spotify_artist_uri', 'biography', 'youtube_url_1', 'youtube_url_2', 'image_url', 'recommended_album')

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ('album_artist', 'album_name', 'release_date', 'genre', 'spotify_albums_uri', 'editors_notes', 'image_url')
