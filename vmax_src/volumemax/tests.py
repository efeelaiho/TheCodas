from django.test import TestCase
from datetime import date
from models import Artist, Albums
# Create your tests here.

class AnimalTestCase(TestCase):
         
    # ----
    # Artist
    # ----

    def test_artists1(self):
        date = datetime.date(1977,6,8)
        a = Artist.objects.create(first_name ="Kanye", last_name = "West", date_of_birth = date, origin = "Chicago, IL")
        self.assertEqual(a.first_name, "Kanye")
        self.assertEqual(a.last_name, "West")
        self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago, IL")

    def test_artists2(self):
        date = datetime.date(1972,10,17)
        a = Artist.objects.create(first_name ="Eminem", date_of_birth = date, origin = "St. Joseph, MO")
        self.assertEqual(a.first_name, "Eminem")
        self.assertEqual(a.date_of_birth, date(1972,10,17))
        self.assertEqual(a.origin, "St. Joseph, MO")

    def test_artists3(self):
        date = datetime.date(1958,8,29)
        a = Artist.objects.create(first_name ="Michael", last_name = "Jackson", date_of_birth = date, origin = "Gary, IN")
        self.assertEqual(a.first_name, "Michael")
        self.assertEqual(a.last_name, "Jackson")
        self.assertEqual(a.date_of_birth, date(1958,8,29))
        self.assertEqual(a.origin, "Chicago, IL")

    # ----
    # Albums
    # ----

    def test_albums1(self): 
        date = datetime.date(1987,9,7)
        a = Albums.objects.create(name = "Bad", artist = "Michael Jackson", release_date = date, genre = "Pop")
        self.assertEqual(a.name, "Bad")
        self.assertEqual(a.artist, "Michael Jackson")
        self.assertEqual(a.release_date, date(1987,9,7))
        self.assertEqual(a.genre, "Pop")

    def test_albums2(self): 
        date = datetime.date(2004,11,12)
        a = Albums.objects.create(name = "Encore", artist = "Eminem", release_date = date, genre = "Hip hop")
        self.assertEqual(a.name, "Encore")
        self.assertEqual(a.artist, "Eminem")
        self.assertEqual(a.release_date, date(2004,11,12))
        self.assertEqual(a.genre, "Hip hop")

    def test_albums3(self): 
        date = datetime.date(2004,2,10)
        a = Albums.objects.create(name = "The College Dropout", artist = "Kanye West", release_date = date, genre = "Hip hop")
        self.assertEqual(a.name, "The College Dropout")
        self.assertEqual(a.artist, "Kanye West")
        self.assertEqual(a.release_date, date(2004,2,10))
        self.assertEqual(a.genre, "Hip hop")


if __name__ == "__main__" :
    main()