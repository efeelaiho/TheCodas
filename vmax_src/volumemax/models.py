from django.db import models

class Artist(models.Model):
	"""
	each artist will contain first_name, last_name, date_of_birth, and origin
	date_of_birth will be represented as a datetime object in YYYY/MM/DD format
	origin will be represented as city, state format (Austin, TX)
	"""
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	date_of_birth = models.DateField()
	origin = models.CharField(max_length=50)
	

class Albums(models.Model):
	"""
	each album will contain artist, name, release_date, and genre
	release_date will be represented as a datetime object in YYYY/MM/DD format
	"""
	artist = models.ForeignKey(Artist)
	name = models.CharField(max_length=100)
	release_date = models.DateField()
	genre = models.CharField(max_length=50)

