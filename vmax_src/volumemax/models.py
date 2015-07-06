from django.db import models

# Create your models here.
class Artist(models.Model):
	first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

class Albums(models.Model):
	artist = models.ForeignKey(Artist)
    name = models.CharField(max_length=100)
    release_date = models.DateField()

class TopSongs(models.Model): 
	artist = models.ForeignKey(Artist)
	album = models.ForeignKey(Albums)
	year = models.DateField()


