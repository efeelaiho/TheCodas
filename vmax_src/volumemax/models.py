from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

class Artist(models.Model):
	"""
	each artist will contain first_name, last_name, date_of_birth, and origin
	date_of_birth will be represented as a datetime object in YYYY/MM/DD format
	origin will be represented as city, state format (Austin, TX)
	get_absolute_url function creates a url link for the artist
	__str__ function returns the artist's name as a string
	"""

	full_name = models.CharField(max_length=100,null=True, blank=True)
	origin = models.CharField(max_length=50,null=True, blank=True)
	popularity = models.IntegerField(null=True, blank=True)
	genre = models.CharField(max_length=50, null=True, blank=True)
	spotify_artist_uri = models.CharField(max_length=500, null=True, blank=True)
	biography = models.CharField(max_length=5000, null=True, blank=True)
	youtube_url_1 = models.CharField(max_length=500, null=True, blank=True)
	youtube_url_2 = models.CharField(max_length=500, null=True, blank=True)
	image_url = models.CharField(max_length=500, null=True, blank=True)
	recommended_album = models.ForeignKey('Album',default=1)

	def get_absolute_url(self):
		url_name = self.full_name.replace(' ', '_')
		return url_name

	def __str__ (self):
		return self.full_name

class Album(models.Model):
	"""
	each album will contain artist, name, release_date, and genre
	release_date will be represented as a datetime object in YYYY/MM/DD format
	get_absolute_url function creates a url link for the album
	__str__ function returns the album name as a string
	"""
	album_artist = models.ForeignKey('Artist',default=1)
	album_name = models.CharField(max_length=100, null=True, blank=True)
	release_date = models.DateField(null=True, blank=True)
	genre = models.CharField(max_length=50, null=True, blank=True)
	spotify_albums_uri = models.CharField(max_length=500, null=True, blank=True)
	editors_notes = models.CharField(max_length=5000, null=True, blank=True)
	image_url = models.CharField(max_length=500, null=True, blank=True)
	
	def get_absolute_url(self):
		url_name = self.album_name.replace(' ', '_')
		return url_name

	def __str__ (self):
		return self.album_name
