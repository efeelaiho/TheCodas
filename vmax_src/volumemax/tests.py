import os
import sys
import json
from django.test.utils import setup_test_environment
from django.utils import unittest

from django.core.urlresolvers import reverse
from django.core.management import call_command

from django.test import TestCase
import datetime
from datetime import date
from volumemax.models import *
from volumemax.search import *

try:
    from urllib.request import urlopen, Request
except:
    from urllib2 import *

from json import dumps, loads

class SearchTestCase(TestCase):

    # -------------
    # Normalization
    # -------------

    def test_normalize_terms1(self):
        query = 'each term, should? be -separate'
        terms = normalize_query(query)
        self.assertEqual(terms, ['each','term,','should?','be','-separate'])

    def test_normalize_terms2(self):
        query = '  some random  words "with   quotes  " and   spaces'
        terms = normalize_query(query)
        self.assertEqual(terms, ['some', 'random', 'words', 'with quotes', 'and', 'spaces'])

    def test_normalize_terms3(self):
        query = ''
        terms = normalize_query(query)
        self.assertEqual(terms, [])

    def test_normalize_terms4(self):
        query = 'isnt is crystal clear'
        terms = normalize_query(query)
        self.assertEqual(terms, ['isnt','it','crystal','clear'])

    def test_normalize_terms5(self):
        query = ' " "   "  '
        terms = normalize_query(query)
        self.assertEqual(terms, [])

    def test_normalize_terms4(self):
        query = 'what are you trying to find'
        terms = normalize_query(query)
        self.assertEqual(terms, ['what','are','you','trying','to','find'])

    def test_normalize_terms5(self):
        query = 'this class is hard'
        terms = normalize_query(query)
        self.assertEqual(terms, ['this','class','is','hard'])

    def test_normalize_terms6(self):
        query = 'this class is okay'
        terms = normalize_query(query)
        self.assertEqual(terms, ['this','class','is','okay'])            

    def test_normalize_terms7(self):
        query = 'hello hello hello hello'
        terms = normalize_query(query)
        self.assertEqual(terms, ['hello','hello','hello','hello'])
    # ---------
    # Searching
    # ---------

    def test_search_nonexistent(self):
        artist = Artist.objects.filter(get_query('and', "Board to Base", ['full_name']))
        self.assertEqual(list(artist),[])

    # def test_search_nonexistent2(self):
    #     artist = Artist.objects.filter(get_query('and', " ", ['full_name']))
    #     self.assertEqual(list(artist),[])

    def test_search_and_artist(self):
        a = Artist.objects.create(full_name ="Jordan", origin = "Chicago, IL", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        b = Artist.objects.create(full_name ="Michael Jackson", origin = "Gary, IN", popularity = 90, genre = "Pop", biography = "asdf")

        artist = Artist.objects.filter(get_query('and', "Michael Jordan", ['full_name']))
        self.assertEqual(list(artist),[])

    def test_search_or_artist(self):
        b = Artist.objects.create(full_name ="Michael Jackson", origin = "Gary, IN", popularity = 90, genre = "Pop", biography = "asdf")
        a = Artist.objects.create(full_name ="John Jordan", origin = "Chicago, IL", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")

        db = 'Michael Jackson'
        #db =  "<Q: (OR: ('full_name__icontains', 'Michael'), ('full_name__icontains', 'Jordan'))>"
        artist = Artist.objects.filter(get_query('or', "Michael Jordan", ['full_name']))
        #artist = list(get_query('or', "Michael Jordan", ['full_name']))
        self.assertEqual(artist[0].full_name,db)  

    def test_search_and_album(self):
        date = 1987

        mj = Artist.objects.create(full_name = "Michael Jackson")
        a = Album.objects.create(album_name = "Bad", album_artist = mj, release_date = date, genre = "Pop", editors_notes = "abc")
        kanye = Artist.objects.create(full_name = "Kanye West")
        b = Album.objects.create(album_name = "College Dropout", album_artist = kanye, release_date = date, genre = "Hip hop", editors_notes = "asdf")
        
        album = Album.objects.filter(get_query('and', "Bad Dropout", ['album_name']))
        self.assertQuerysetEqual(list(album),[])

    def test_search_or_album(self):
        date = 1987

        kanye = Artist.objects.create(full_name = "Kanye West")
        b = Album.objects.create(album_name = "College Dropout", album_artist = kanye, release_date = date, genre = "Hip hop", editors_notes = "asdf")
        mj = Artist.objects.create(full_name = "Michael Jackson")
        a = Album.objects.create(album_name = "Bad", album_artist = mj, release_date = date, genre = "Pop", editors_notes = "abc")

        db = 'College Dropout'
        album = Album.objects.filter(get_query('or', "DroPOUt Bad", ['album_name']))
        # self.assertQuerysetEqual(list(album),['<Album: Bad>','<Album: The College Dropout>'])
        self.assertEqual(album[0].album_name,db)


class ArtistTestCase(TestCase):
         
    # ----
    # Artist
    # ----

    def test_artists1(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Kanye West", origin = "Chicago, IL", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        self.assertEqual(a.full_name, "Kanye West")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago, IL")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Rap, Hip Hop")
        self.assertEqual(a.biography, "abc")

    def test_artists2(self):
        # date = datetime.date(1972,10,17)
        a = Artist.objects.create(full_name ="Eminem", origin = "St. Joseph, MO", popularity = 96, genre = "Rap, Hip Hop", biography = "123")
        self.assertEqual(a.full_name, "Eminem")
        # self.assertEqual(a.date_of_birth, date(1972,10,17))
        self.assertEqual(a.origin, "St. Joseph, MO")
        self.assertEqual(a.popularity, 96)
        self.assertEqual(a.genre, "Rap, Hip Hop")
        self.assertEqual(a.biography, "123")

    def test_artists3(self):
        # date = datetime.date(1958,8,29)
        a = Artist.objects.create(full_name ="Michael Jackson", origin = "Gary, IN", popularity = 90, genre = "Pop", biography = "asdf")
        self.assertEqual(a.full_name, "Michael Jackson")
        # self.assertEqual(a.date_of_birth, date(1958,8,29))
        self.assertEqual(a.origin, "Gary, IN")
        self.assertEqual(a.popularity, 90)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.biography, "asdf")

    def test_artists4(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Rihanna", origin = "Saint Michael, Barbados", popularity = 97, genre = "Pop", biography = "qwerty")
        self.assertEqual(a.full_name, "Rihanna")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Saint Michael, Barbados")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.biography, "qwerty")

    def test_artists5(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Queen", origin = "London, United Kingdom", popularity = 87, genre = "Rock", biography = "azerty")
        self.assertEqual(a.full_name, "Queen")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "London, United Kingdom")
        self.assertEqual(a.popularity, 87)
        self.assertEqual(a.genre, "Rock")
        self.assertEqual(a.biography, "azerty")


    def test_artists6(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Elvis Presley", origin = "Tupelo, Mississippi", popularity = 82, genre = "Rock", biography = "elvis is cool")
        self.assertEqual(a.full_name, "Elvis Presley")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Tupelo, Mississippi")
        self.assertEqual(a.popularity, 82)
        self.assertEqual(a.genre, "Rock")
        self.assertEqual(a.biography, "elvis is cool")

    def test_artists7(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Britney Spears", origin = "McComb, Mississippi", popularity = 86, genre = "Pop", biography = "clown")
        self.assertEqual(a.full_name, "Britney Spears")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "McComb, Mississippi")
        self.assertEqual(a.popularity, 86)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.biography, "clown")

    def test_artists8(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Efe", origin = "Chicago, IL", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        self.assertEqual(a.full_name, "Efe")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago, IL")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Rap, Hip Hop")
        self.assertEqual(a.biography, "abc")

    def test_artists9(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="Elaiho", origin = "Chicago", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        self.assertEqual(a.full_name, "Elaiho")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Rap, Hip Hop")
        self.assertEqual(a.biography, "abc")

    def test_artists10(self):
        # date = datetime.date(1977,6,8)
        a = Artist.objects.create(full_name ="ElaihoEfe", origin = "Chicago", popularity = 97, genre = "Rap, Hip Hop", biography = "abc")
        self.assertEqual(a.full_name, "ElaihoEfe")
        # self.assertEqual(a.date_of_birth, date(1977,6,8))
        self.assertEqual(a.origin, "Chicago")
        self.assertEqual(a.popularity, 97)
        self.assertEqual(a.genre, "Rap, Hip Hop")
        self.assertEqual(a.biography, "abc")

    

    # ----
    # Albums
    # ----

    def test_albums1(self): 
        mj = Artist.objects.create(full_name = "Michael Jackson")
        a = Album.objects.create(album_name = "Bad", album_artist = mj, release_date = 1987, genre = "Pop", editors_notes = "abc")
        self.assertEqual(a.album_name, "Bad")
        self.assertEqual(a.album_artist, mj)
        self.assertEqual(a.release_date, 1987)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.editors_notes, "abc")

    def test_albums2(self): 
        Eminem = Artist.objects.create(full_name = "Eminem")
        a = Album.objects.create(album_name = "Encore", album_artist = Eminem, release_date = 2004, genre = "Hip hop", editors_notes = "123")
        self.assertEqual(a.album_name, "Encore")
        self.assertEqual(a.album_artist, Eminem)
        self.assertEqual(a.release_date, 2004)
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "123")

    def test_albums3(self): 
        kanye = Artist.objects.create(full_name = "Kanye West")
        a = Album.objects.create(album_name = "The College Dropout", album_artist = kanye, release_date = 2004, genre = "Hip hop", editors_notes = "asdf")
        self.assertEqual(a.album_name, "The College Dropout")
        self.assertEqual(a.album_artist, kanye)
        self.assertEqual(a.release_date, 2004)
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "asdf")

    def test_albums4(self): 
        mariah = Artist.objects.create(full_name = "Mariah Carey")
        a = Album.objects.create(album_name = "Daydream", album_artist = mariah, release_date = 1995, genre = "R&B", editors_notes = "crystal clear")
        self.assertEqual(a.album_name, "Daydream")
        self.assertEqual(a.album_artist, mariah)
        self.assertEqual(a.release_date, 1995)
        self.assertEqual(a.genre, "R&B")
        self.assertEqual(a.editors_notes, "crystal clear")

    def test_albums5(self): 
        acdc = Artist.objects.create(full_name = "AC/DC")
        a = Album.objects.create(album_name = "Back In Black", album_artist = acdc, release_date = 1980, genre = "Rock", editors_notes = "hello world")
        self.assertEqual(a.album_name, "Back In Black")
        self.assertEqual(a.album_artist, acdc)
        self.assertEqual(a.release_date, 1980)
        self.assertEqual(a.genre, "Rock")
        self.assertEqual(a.editors_notes, "hello world")


    def test_albums6(self): 
        pharrell = Artist.objects.create(full_name = "Pharrell Williams")
        a = Album.objects.create(album_name = "G I R L", album_artist = pharrell, release_date = 2014, genre = "Hip-Hop/Rap", editors_notes = "gpdowning")
        self.assertEqual(a.album_name, "G I R L")
        self.assertEqual(a.album_artist, pharrell)
        self.assertEqual(a.release_date, 2014)
        self.assertEqual(a.genre, "Hip-Hop/Rap")
        self.assertEqual(a.editors_notes, "gpdowning")

    def test_albums7(self): 
        pharrell = Artist.objects.create(full_name = "Pharrell Williams")
        a = Album.objects.create(album_name = "G I R L", album_artist = cake, release_date = 1993, genre = "Hip-Hop/Rap", editors_notes = "byoung")
        self.assertEqual(a.album_name, "G I R L")
        self.assertEqual(a.album_artist, cake)
        self.assertEqual(a.release_date, 1993)
        self.assertEqual(a.genre, "Hip-Hop/Rap")
        self.assertEqual(a.editors_notes, "byoung")


    def test_albums8(self): 
        pharrell = Artist.objects.create(full_name = "Pharrell Williams")
        a = Album.objects.create(album_name = "crash", album_artist = cake, release_date = 13, genre = "Hip-Hop/Rap", editors_notes = "byoung")
        self.assertEqual(a.album_name, "crash")
        self.assertEqual(a.album_artist, cake)
        self.assertEqual(a.release_date, 13)
        self.assertEqual(a.genre, "Hip-Hop/Rap")
        self.assertEqual(a.editors_notes, "byoung")

# ------------------
# API Tests
# ------------------


class APItests(unittest.TestCase) :
    url = "http://127.0.0.1:8000/"

    #----
    #Artists
    #----

    def test_get_artist1(self) :
        request = Request(self.url+"api/artists/16")
        expected_api ={"full_name":"Eminem","origin":" St. Joseph, Missouri","popularity":96,"genre":"Hip-Hop/Rap","spotify_artist_uri":"spotify:artist:7dGJo4pcD2V6oG8kP0tJRR","biography":"Marshall Bruce Mathers III (born October 17, 1972), better known by his stage name Eminem, is an American rapper, record producer, and songwriter from Detroit, Michigan. In addition to his solo career, he is a member of D12 and (with Royce da 5'9\") half of the hip-hop duo Bad Meets Evil. Eminem is the best-selling artist of the 2000s in the United States; Rolling Stone ranked him 83rd on its list of 100 Greatest Artists of All Time, calling him the King of Hip Hop. Including his work with D12 and Bad Meets Evil, Eminem has had ten number-one albums on the Billboard 200. He has sold more than 155 million albums and singles, making him one of the world's best-selling artists. As of June 2014, Eminem is the second-bestselling male artist of the Nielsen SoundScan era, the sixth-bestselling artist in the United States and the bestselling hip-hop artist, with sales of 45,160,000 albums and 31 million digital singles.\nAfter his debut album Infinite (1996), Eminem achieved mainstream popularity in 1999 with The Slim Shady LP; the commercially successful second album received his first Grammy Award for Best Rap Album. His next two releases (2000's The Marshall Mathers LP and 2002's The Eminem Show) were worldwide successes, with each certified diamond in US sales. Both won Best Rap Album Grammy Awards, making Eminem the first artist to win the award for three consecutive LPs. They were followed by Encore in 2004, another critical and commercial success. Eminem went on hiatus after touring in 2005, releasing Relapse in 2009 and Recovery in 2010; both won Grammy Awards. Recovery was the bestselling album of 2010 worldwide, and the rapper's second international bestselling album of the year (his first was The Eminem Show). Eminem's eighth album (2013's The Marshall Mathers LP 2) won two Grammy Awards, including Best Rap Album; it expanded his record for the most wins in that category and his Grammy total to 15.\nEminem has developed other ventures, including Shady Records with manager Paul Rosenberg. He has his own channel, Shade 45, on Sirius XM Radio. In November 2002, Eminem starred in the hip hop film 8 Mile. He won the Academy Award for Best Original Song for \"Lose Yourself\", the first rap artist to win the award. Eminem has made cameo appearances in the films The Wash (2001), Funny People (2009), The Interview (2014) and the television series Entourage.","youtube_url_1":"https://www.youtube.com/embed/0AqnCSdkjQ0","youtube_url_2":"https://www.youtube.com/embed/XbGs_qK2PQA","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/f08ed487e3894e0f9ab1c199cbd449d0fb7e244c","recommended_album":16}
        api = urlopen(request)
        api_body = api.read().decode("utf-8")
        self.assertEqual(api.getcode(), 200)
        api_data = loads(api_body)

        unmatched_item = set(api_data) ^ set(expected_api)
        self.assertEqual(len(unmatched_item), 0)


    def test_get_artist2(self) :
        request = Request(self.url+"api/artists/113")
        expected_api ={
        "full_name": "Kanye West",
        "origin": "Chicago, IL",
        "popularity": 97,
        "genre": "Hip-Hop/Rap",
        "spotify_artist_uri": "spotify:artist:5K4W6rqBFWDnAN6FQUkS6x",
        "biography": "Kanye Omari West (/\u02c8k\u0251\u02d0nje\u026a/; born June 8, 1977) is an American rapper, songwriter, record producer and fashion designer. West first became known as a producer for Roc-A-Fella Records; he achieved recognition for his work on rapper Jay-Z's The Blueprint (2001), as well as hit singles for musical artists including Alicia Keys, Ludacris, and Janet Jackson. His style of production originally used high-pitched vocal samples from soul songs incorporated with his own drums and instruments. He later broadened his influences to include 1970s R&B, baroque pop, trip hop, arena rock, house, folk, alternative, electronica, synthpop, industrial, and classical music.\nWest was raised in a middle-class household in Chicago, Illinois, and began rapping in the third grade, becoming involved in the city's hip hop scene. West attended art school for one semester before dropping out to pursue music entirely in the late 1990s. Although his real desire was to become a rapper, record executives did not take West seriously, viewing him as a producer first and foremost. After being signed to Roc-A-Fella in 2002, West released his debut album The College Dropout in 2004 to commercial and critical acclaim. The baroque-inspired Late Registration followed in 2005, and Graduation in 2007. West switched rapping for singing on his emotive 2008 effort 808's & Heartbreak, and embraced maximalism on 2010's My Beautiful Dark Twisted Fantasy. Following several collaborations, West released his abrasive sixth album, Yeezus, in 2013.\nWest is one of the best- selling artists of all time, having sold more than 21 million albums and 100 million digital downloads. He has won a total of 21 Grammy Awards, making him one of the most awarded artists of all- time and the most Grammy-awarded artist of his age. Time named West one of the 100 most influential people in the world in 2005, 2011 and 2015. He has also been included in a number of Forbes annual lists. Three of his albums rank on Rolling Stone's 2012 \"500 Greatest Albums of All Time\" list; two of his albums feature at #8 and #1 in Pitchfork Media's The 100 Best Albums of 2010\u20132014.\nWest's background and style, from his debut album, deviated from the then-dominant \"gangsta\" persona in hip hop, and he would later alter the genre stylistically as rappers adopted his alternative aesthetic. An outspoken and controversial celebrity, West has often been a source of controversy due to his appearances at award shows and his various television and radio interviews. West has collaborated on multiple occasions with brands Nike, Louis Vuitton, Adidas and A.P.C.. West also runs his own record label GOOD Music and has directed several short films.",
        "youtube_url_1": "https://www.youtube.com/embed/Co0tTeuUVhU",
        "youtube_url_2": "https://www.youtube.com/embed/PsO6ZnUZI0g",
        "recommended_album": 113,
        "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/fca17e83545e076fafb561569e8d5ec64f87eb8c"
        }
        api = urlopen(request)
        api_body = api.read().decode("utf-8")
        self.assertEqual(api.getcode(), 200)
        api_data = loads(api_body)
        self.assertEqual(api_data, expected_api)

    def test_get_artist3(self) :
        request = Request(self.url+"api/artists/54")
        expected_api = {"full_name":"Evanescence","origin":" Little Rock, Arkansas, United States","popularity":76,"genre":"Rock","spotify_artist_uri":"spotify:artist:5nGIFgo0shDenQYSE0Sn7c","biography":"Evanescence is an American rock band founded in Little Rock, Arkansas in 1995 by singer/pianist Amy Lee and guitarist Ben Moody. After recording independent albums, the band released their first full-length album, Fallen, on Wind-up Records in 2003. Fallen sold more than 17 million copies worldwide and helped the band win two Grammy Awards and seven nominations, as well as scoring No. 6 in CBS's \"Top Bestselling Albums of the Last 10 Years\" (2008). A year later, Evanescence released their first live album, Anywhere but Home, which sold more than one million copies worldwide. In 2006, the band released their second studio album, The Open Door, which sold more than five million copies.\nThe line-up of the group has changed several times: David Hodges leaving in 2002, co-founder Moody left in 2003 (mid-tour), bassist Will Boyd in 2006, followed by guitarist John LeCompt and drummer Rocky Gray in 2007. The last two changes led to a hiatus, with temporary band members contributing to tour performances. Billboard ranked Evanescence No. 71 on the Best Artists of the Decade chart.\nAnnounced in June 2009, the newest line-up of the band eventually returned with Evanescence, their self-titled third studio album, released on October 11, 2011. It debuted at No. 1 on the Billboard 200 chart with 127,000 copies in sales. The album also debuted at No. 1 on four other different Billboard charts; the Rock Albums, Digital Albums, Alternative Albums, and the Hard Rock Albums charts. The band spent 2012 on tour in promotion of their new album with other bands including The Pretty Reckless and Fair to Midland.","youtube_url_1":"https://www.youtube.com/embed/5anLPw0Efmo","youtube_url_2":"https://www.youtube.com/embed/CdhqVtpR2ts","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/51aaff58f3fa23591eb9fbf9316aff7e551b586a","recommended_album":54}
        api = urlopen(request)
        api_body = api.read().decode("utf-8")
        self.assertEqual(api.getcode(), 200)
        api_data = loads(api_body)
        self.assertEqual(api_data, expected_api)

    def test_get_artist4(self) :
        request = Request(self.url+"api/artists/25")
        expected_api = {"full_name":"Genesis","origin":"Godalming, Surrey","popularity":71,"genre":"Rock","spotify_artist_uri":"spotify:artist:3CkvROUTQ6nRi9yQOcsB50","biography":"Not available","youtube_url_1":"https://www.youtube.com/embed/1pkVLqSaahk","youtube_url_2":"https://www.youtube.com/embed/pW68T84RLHw","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/147c67b0c8e6248d46b11db586be1ba0f5e2b3d3","recommended_album":25}
        api = urlopen(request)
        api_body = api.read().decode("utf-8")
        self.assertEqual(api.getcode(), 200)
        api_data = loads(api_body)
        self.assertEqual(api_data, expected_api)

    #----
    #Albums
    #----
    def test_get_album1(self) :
        request = Request(self.url+"api/albums/16")
        expected_api = {"album_artist":16,"album_name":"The Eminem Show","release_date":2002,"genre":"Hip-Hop/Rap","spotify_albums_uri":"spotify:album:2cWBwpqMsDJC1ZUwz813lo","editors_notes":"On the follow-up to The Marshall Mathers LP, Eminem set out to broaden his already wide artistic horizons. He makes his most overt nods yet to rock music, borrowing Aerosmith's \"Dream On\" for the basis of \"Sing for the Moment,\" and gets explicitly political about his job on \"White America\" (\"I could be one of your kids\"). At the same time, he takes himself no more seriously than usual, mocking any hint of grandiosity on \"My Dad's Gone Crazy,\" which invites his beloved daughter Hailie to take funny shots at the old man. \"Superman\" pulls a similar trick not only with the rapper's image, but the macho pose intrinsic to commercial hip-hop.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/1f881110ff752c80069da0308b1de30196d4f8a1"}
        response = urlopen(request)
        response_body = response.read().decode("utf-8")
        self.assertEqual(response.getcode(), 200)
        api_data = loads(response_body)
        self.assertEqual(api_data, expected_api)

    def test_get_album2(self) :
        request = Request(self.url+"api/albums/113")
        expected_api = {"album_artist":113,"album_name":"College Dropout","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:3ff2p3LnR6V7m6BinwhNaQ","editors_notes":"Kanye West gained notoriety as a producer-for-hire before The College Dropout shook hip-hop to its core. The mix of styles and subject matter is breathtaking. Pop hits rub up against vulnerable moments. Street anthems mingle with wild humor. And \"Jesus Walks\" challenges beliefs like no other rap song before it. Kanye West attacks the set with confidence and conviction.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/102504bd8952b26857974a3dab5884430245e228"}
        response = urlopen(request)
        response_body = response.read().decode("utf-8")
        self.assertEqual(response.getcode(), 200)
        api_data = loads(response_body)
        self.assertEqual(api_data, expected_api)

    def test_get_album3(self) :
        request = Request(self.url+"api/albums/25")
        expected_api = {"album_artist":25,"album_name":"Invisible Touch","release_date":1986,"genre":"Rock","spotify_albums_uri":"spotify:album:632b0oXuFpstA4DO2cUKdG","editors_notes":"Not available","image_url":"https://i.scdn.co/image/431343e6995d6b71cc700fd24d18f336dfcbe61a"}
        response = urlopen(request)
        response_body = response.read().decode("utf-8")
        self.assertEqual(response.getcode(), 200)
        api_data = loads(response_body)
        self.assertEqual(api_data, expected_api)

    def test_get_album4(self) :
        request = Request(self.url+"api/albums/54")
        expected_api = {"album_artist":54,"album_name":"Fallen","release_date":2003,"genre":"Rock","spotify_albums_uri":"spotify:album:02w1xMzzdF2OJxTeh1basm","editors_notes":"Fallen is the debut studio album by American rock band Evanescence. It was released on March 4, 2003, through Wind-up Records and Epic Records.[4] The album was recorded in multiple recording studios, including Conway Recording Studios in Hollywood, California. It is commercially the band's most successful album to date, selling more than seven million copies in the United States alone, and more than 17 million worldwide. It debuted at number 7 on the Billboard 200, selling more than 141,000 copies within its first week, eventually peaking at number 3 in June 2003. Internationally, it topped the charts in more than ten countries. It was certified Platinum seven times by the Recording Industry Association of America (RIAA), and acquired multiple certifications worldwide.\nUpon its release, Fallen received mixed to positive reviews from music critics. It spawned four singles: \"Bring Me to Life\", \"My Immortal\", \"Going Under\", and \"Everybody's Fool\". \"Bring Me to Life\" and \"My Immortal\" peaked within the charts of more than ten countries, including Australia, the United Kingdom, and the United States. The album earned the band five nominations at the 46th Grammy Awards: Album of the Year, Best Rock Album, Best Rock Song, Best Hard Rock Performance and Grammy Award for Best New Artist, winning Best New Artist and Best Hard Rock Performance.","image_url":"https://i.scdn.co/image/a42e3ae40dfd871b5d17a00f2f8167c0d0d26916"}
        response = urlopen(request)
        response_body = response.read().decode("utf-8")
        self.assertEqual(response.getcode(), 200)
        api_data = loads(response_body)
        self.assertEqual(api_data, expected_api)


        # for album1, album2 in zip(api_data, expected_api):
        #     unmatched_item = set(album1.items()) ^ set(album2.items())
        #     self.assertEqual(len(unmatched_item), 0)

if __name__ == "__main__" :
    main()