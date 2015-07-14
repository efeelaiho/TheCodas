import os
import sys
import json
from django.test.utils import setup_test_environment
from django.core.urlresolvers import reverse
from django.core.management import call_command

from django.test import TestCase
from datetime import date
from models import Artist, Albums

from json import dumps, loads

class AnimalTestCase(TestCase):
         
    # ----
    # Artist
    # ----

    def test_artists1(self):
        date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Kanye West", date_of_birth = date, origin = "Chicago, IL", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        self.assertEqual(a.full_name, "Kanye West")
        self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago, IL")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Rap, Hip hop")
        self.assertEqual(a.biography, "abc")

    def test_artists2(self):
        date = datetime.date(1972,10,17)
        a = Artist.objects.create(full_name ="Eminem", date_of_birth = date, origin = "St. Joseph, MO", popularity = 96, genre = "Rap, Hip Hop", biography = "123")
        self.assertEqual(a.full_name, "Eminem")
        self.assertEqual(a.date_of_birth, date(1972,10,17))
        self.assertEqual(a.origin, "St. Joseph, MO")
        self.assertEqual(a.popularity, 96)
        self.assertEqual(a.genre, "Rap, Hip hop")
        self.assertEqual(a.biography, "123")

    def test_artists3(self):
        date = datetime.date(1958,8,29)
        a = Artist.objects.create(full_name ="Michael Jackson", date_of_birth = date, origin = "Gary, IN", popularity = 90, genre = "Pop", biography = "asdf")
        self.assertEqual(a.full_name, "Michael Jackson")
        self.assertEqual(a.date_of_birth, date(1958,8,29))
        self.assertEqual(a.origin, "Chicago, IL")
        self.assertEqual(a.popularity, 90)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.biography, "asdf")

    # ----
    # Albums
    # ----

    def test_albums1(self): 
        date = datetime.date(1987,9,7)
        a = Albums.objects.create(name = "Bad", artist = "Michael Jackson", release_date = date, genre = "Pop", editors_notes = "abc")
        self.assertEqual(a.name, "Bad")
        self.assertEqual(a.artist, "Michael Jackson")
        self.assertEqual(a.release_date, date(1987,9,7))
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.editors_notes, "abc")

    def test_albums2(self): 
        date = datetime.date(2004,11,12)
        a = Albums.objects.create(name = "Encore", artist = "Eminem", release_date = date, genre = "Hip hop", editors_notes = "123")
        self.assertEqual(a.name, "Encore")
        self.assertEqual(a.artist, "Eminem")
        self.assertEqual(a.release_date, date(2004,11,12))
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "123")

    def test_albums3(self): 
        date = datetime.date(2004,2,10)
        a = Albums.objects.create(name = "The College Dropout", artist = "Kanye West", release_date = date, genre = "Hip hop", editors_notes = " asdf")
        self.assertEqual(a.name, "The College Dropout")
        self.assertEqual(a.artist, "Kanye West")
        self.assertEqual(a.release_date, date(2004,2,10))
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "asdf")


if __name__ == "__main__" :
    main()