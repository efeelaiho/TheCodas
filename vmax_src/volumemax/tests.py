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
        query = 'isnt it crystal clear'
        terms = normalize_query(query)
        self.assertEqual(terms, ['isnt','it','crystal','clear'])

    def test_normalize_terms5(self):
        query = ' " "   "  '
        terms = normalize_query(query)
        self.assertEqual(terms, ['', '"'])

    # ---------
    # Searching
    # ---------

    def test_search_nonexistent(self):
        artist = Artist.objects.filter(get_query('and', "Board to Base", ['full_name']))
        self.assertEqual(list(artist),[])

    def test_search_nonexistent2(self):
        artist = Artist.objects.filter(get_query('and', " ", ['full_name']))
        self.assertEqual(list(artist),[])

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

    # ----
    # Albums
    # ----

    def test_albums1(self): 
        date = datetime.date(1987,9,7)
        mj = Artist.objects.create(full_name = "Michael Jackson")
        a = Album.objects.create(album_name = "Bad", album_artist = mj, release_date = 1987, genre = "Pop", editors_notes = "abc")
        self.assertEqual(a.album_name, "Bad")
        self.assertEqual(a.album_artist, mj)
        self.assertEqual(a.release_date, 1987)
        self.assertEqual(a.genre, "Pop")
        self.assertEqual(a.editors_notes, "abc")

    def test_albums2(self): 
        date = datetime.date(2004,11,12)
        Eminem = Artist.objects.create(full_name = "Eminem")
        a = Album.objects.create(album_name = "Encore", album_artist = Eminem, release_date = 2004, genre = "Hip hop", editors_notes = "123")
        self.assertEqual(a.album_name, "Encore")
        self.assertEqual(a.album_artist, Eminem)
        self.assertEqual(a.release_date, 2004)
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "123")

    def test_albums3(self): 
        date = datetime.date(2004,2,10)
        kanye = Artist.objects.create(full_name = "Kanye West")
        a = Album.objects.create(album_name = "The College Dropout", album_artist = kanye, release_date = 2004, genre = "Hip hop", editors_notes = "asdf")
        self.assertEqual(a.album_name, "The College Dropout")
        self.assertEqual(a.album_artist, kanye)
        self.assertEqual(a.release_date, 2004)
        self.assertEqual(a.genre, "Hip hop")
        self.assertEqual(a.editors_notes, "asdf")

    def test_albums4(self): 
        date = datetime.date(1995,9,7)
        mariah = Artist.objects.create(full_name = "Mariah Carey")
        a = Album.objects.create(album_name = "Daydream", album_artist = mariah, release_date = 1995, genre = "R&B", editors_notes = "crystal clear")
        self.assertEqual(a.album_name, "Daydream")
        self.assertEqual(a.album_artist, mariah)
        self.assertEqual(a.release_date, 1995)
        self.assertEqual(a.genre, "R&B")
        self.assertEqual(a.editors_notes, "crystal clear")

    def test_albums5(self): 
        date = datetime.date(1980,5,6)
        acdc = Artist.objects.create(full_name = "AC/DC")
        a = Album.objects.create(album_name = "Back In Black", album_artist = acdc, release_date = 1980, genre = "Rock", editors_notes = "hello world")
        self.assertEqual(a.album_name, "Back In Black")
        self.assertEqual(a.album_artist, acdc)
        self.assertEqual(a.release_date, 1980)
        self.assertEqual(a.genre, "Rock")
        self.assertEqual(a.editors_notes, "hello world")



# ------------------
# API Tests
# ------------------


class APItests(unittest.TestCase) :
    url = "http://127.0.0.1:8000/"

    #----
    #Artists
    #----

    def test_get_all_artists(self) :
        request = Request(self.url+"api/artists/")
        expected_api =[
        {
            "full_name":"Eminem",
            "origin":"Chicago, IL" ,
            "popularity":96,
            "genre":"Hip-Hop/Rap",
            "spotify_artist_uri":"spotify:artist:7dGJo4pcD2V6oG8kP0tJRR",
            "biography":"Marshall Bruce Mathers III (born October 17, 1972), better known by his stage name Eminem, is an American rapper, record producer, and songwriter from Detroit, Michigan. In addition to his solo career, he is a member of D12 and (with Royce da 5'9\") half of the hip-hop duo Bad Meets E vil. Eminem is the best-selling artist of the 2000s in the United States; Rolling Stone ranked h im 83rd on its list of 100 Greatest Artists of All Time, calling him the King of Hip Hop. Includ ing his work with D12 and Bad Meets Evil, Eminem has had ten number-one albums on the Billboard 200. He has sold more than 155 million albums and singles, making him one of the world's best-s elling artists. As of June 2014, Eminem is the second-bestselling male artist of the Nielsen So undScan era, the sixth-bestselling artist in the United States and the bestselling hip-hop arti st, with sales of 45,160,000 albums and 31 million digital singles.\nAfter his debut album Inf inite (1996), Eminem achieved mainstream popularity in 1999 with The Slim Shady LP; the commer cially successful second album received his first Grammy Award for Best Rap Album. His next tw o releases (2000's The Marshall Mathers LP and 2002's The Eminem Show) were worldwide successe s, with each certified diamond in US sales. Both won Best Rap Album Grammy Awards, making Emine the first artist to win the award for three consecutive LPs. They were followed by Encore in 2004, another critical and commercial success. Eminem went on hiatus after touring in 2005, releasing Relapse in 2009 and Recovery in 2010; both won Grammy Awards. Recovery was the b estselling album of 2010 worldwide, and the rapper's second international bestselling alb um of the year (his first was The Eminem Show). Eminem's eighth album (2013's The Marshall Mathers LP 2) won two Grammy Awards, including Best Rap Album; it expanded his record fo r the most wins in that category and his Grammy total to 15.\nEminem has developed other ventu res, including Shady Records with manager Paul Rosenberg. He has his own channel, Shade 45, on Sirius XM Radio. In November 2002, Eminem starred in the hip hop film 8 Mile. He won the Acad emy Award for Best Original Song for \"Lose Yourself\", the first rap artist to win the award . Eminem has made cameo appearances in the films The Wash (2001), Funny People (2009), The In terview (2014) and the television series Entourage.",
            "youtube_url_1":"https://www.youtube.com/embed/S9bCLPwzSC0",
            "youtube_url_2":"https://www.youtube.com/embed/uelHwf8o7_U",
            "recommended_album":1,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/f08ed487e3894e0f9ab1c199cbd449d0fb7e244c"
        },
        {
            "full_name":"Kanye West",
            "origin":"Chicago, IL",
            "popularity":97,
            "genre":"Hip-Hop/Rap",
            "spotify_artist_uri":"spotify:artist:5K4W6rqBFWDnAN6FQUkS6x",
            "biography":"Kanye Omari West (/\u02c8k\u0251\u02d0nje\u026a/; born June 8, 1977) is an American rapper, songwriter, record producer and fashion designer. West first became known as a producer for Roc-A-Fella Records; he achieved recognition for his work on rapper Jay-Z's The Blueprint (2001), as well as hit singles for musical artists including Alicia Keys, Ludacris, and Janet Jackson. His style of production originally used high-pitched vocal samples from soul songs incorporated with his own drums and instruments. He later broadened his influences to include 1970s R&B, baroque pop, trip hop, arena rock, house, folk, alternative, electronica, synthpop, industrial, and classical music.\nWest was raised in a middle-class household in Chicago, Illinois, and began rapping in the third grade, becoming involved in the city's hip hop scene. West attended art school for one semester before dropping out to pursue music entirely in the late 1990s. Although his real desire was to become a rapper, record executives did not take West seriously, viewing him as a producer first and foremost. After being signed to Roc-A-Fella in 2002, West released his debut album The College Dropout in 2004 to commercial and critical acclaim. The baroque-inspired Late Registration followed in 2005, and Graduation in 2007. West switched rapping for singing on his emotive 2008 effort 808's & Heartbreak, and embraced maximalism on 2010's My Beautiful Dark Twisted Fantasy. Following several collaborations, West released his abrasive sixth album, Yeezus, in 2013.\nWest is one of the best- selling artists of all time, having sold more than 21 million albums and 100 million digital downloads. He has won a total of 21 Grammy Awards, making him one of the most awarded artists of all- time and the most Grammy-awarded artist of his age. Time named West one of the 100 most influential people in the world in 2005, 2011 and 2015. He has also been included in a number of Forbes annual lists. Three of his albums rank on Rolling Stone's 2012 \"500 Greatest Albums of All Time\" list; two of his albums feature at #8 and #1 in Pitchfork Media's The 100 Best Albums of 2010\u20132014.\nWest's background and style, from his debut album, deviated from the then-dominant \"gangsta\" persona in hip hop, and he would later alter the genre stylistically as rappers adopted his alternative aesthetic. An outspoken and controversial celebrity, West has often been a source of controversy due to his appearances at award shows and his various television and radio interviews. West has collaborated on multiple occasions with brands Nike, Louis Vuitton, Adidas and A.P.C.. West also runs his own record label GOOD Music and has directed several short films.",
            "youtube_url_1":"https://www.youtube.com/embed/Co0tTeuUVhU",
            "youtube_url_2":"https://www.youtube.com/embed/PsO6ZnUZI0g",
            "recommended_album":2,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/fca17e83545e076fafb561569e8d5ec64f87eb8c"
        },
        {            
            "full_name":"Kendrick Lamar",
            "origin":"Compton, CA",
            "popularity":93,
            "genre":"Hip-Hop/Rap",
            "spotify_artist_uri":"spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg",
            "biography":"Platinum-selling, Grammy-nominated rapper Kendrick Lamar is one of the rare artists who has achieved critical and commercial success while earning the respect and support of those who inspired him. A native of Compton, California, Lamar originally rapped as K. Dot and released a series of mixtapes under that name. Youngest Head N***a in Charge (2003), issued when he was only 16 years old, caught the attention of Top Dawg Entertainment and led to a long-term association that helped raise the rapper's profile. Training Day (2005) and C4 (2009) also preceded his decision to go by his birth name. The latter was issued the same year he became part of Black Hippy — beside fellow Top Dawg artists Ab-Soul, Jay Rock, and ScHoolboy Q — a group whose members, for the most part, appeared on one another's mixtapes and albums. Overly Dedicated (2010) was the first Kendrick Lamar mixtape and fared well enough to enter Billboard's R&B/Hip-Hop Albums chart that October. His first official album, Section.80 (2011), was released as a digital download the following year and entered the Billboard 200 at number 113. By that point in his career, Lamar's reputation had been strengthened through guest appearances on dozens of tracks, and he had the support of veteran West Coast stars as well. During a 2011 concert, Dr. Dre, Snoop Dogg, and Game dubbed him \"The New King of the West Coast,\" a notion Dre endorsed more significantly by signing Lamar to the Aftermath label. Lamar's Good Kid, M.A.A.D City was released in October 2012 and debuted at number two on the Billboard 200. Three of its singles — \"Swimming Pools (Drank),\" \"Poetic Justice,\" and \"Bitch Don't Kill My Vibe\" — reached the Top Ten of Billboard's Hot R&B/Hip-Hop chart, with each one enjoying lengthy stays on playlists of urban U.S. radio stations. More significantly, the album showcased Lamar as an exceptional storyteller capable of making compelling concept albums. When the nominees for the 56th Annual Grammy Awards were announced, Lamar was listed in seven categories, including Best New Artist and Album of the Year. He won none of the awards. Rather than rest, Lamar remained active during 2013-2014 with touring as well as appearances on tracks by the likes of Tame Impala, YG, and fellow Top Dawg affiliate SZA. Early in 2015, he announced his third album, To Pimp a Butterfly, was due in March with tracks featuring Snoop Dogg, Bilal, Thundercat, and George Clinton. A technical accident caused the digital album to be released eight days early, but it immediately earned rave reviews and sales of 325,000 copies within its first week of release.", "youtube_url_1": "https://www.youtube.com/embed/Z-48u_uWMHY",
            "youtube_url_2":"https://www.youtube.com/embed/8aShfolR6w8",
            "recommended_album":3,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/710f327a57dff722909bbe1e85d7c8aef88c666e"
        },
        {

            "full_name":"Frank Ocean",
            "origin":"New Orleans, LA",
            "popularity":82,
            "genre":"Hip-Hop/Rap",
            "spotify_artist_uri":"spotify:artist:2h93pZq0e7k5yf4dywlkpM",
            "biography":"An R&B vocalist affiliated with the outlandish hip-hop crew Odd Future Wolf Gang Kill Them All, Frank Ocean (Christopher \"Lonny\" Breaux) was born and raised in New Orleans. The aspiring songwriter and singer had just moved into his dorm at the University of New Orleans when Hurricane Katrina hit. With his future under water, Ocean immediately left the academic life behind and moved to L.A. to give music a shot. He cut some demos at a friend's home studio, shopped them around town, and eventually landed a songwriting deal that would find him working for Justin Bieber, John Legend, and Brandy. Some of this work was alongside Christopher \"Tricky\" Stewart, a fellow songwriter and producer who would convince Ocean to sign a solo artist deal with Def Jam in late 2009. It was also around this time he met Odd Future and began writing music for the crew while making guest appearances on their mixtapes. In February 2011, as Odd Future were making waves, Ocean broke out on his own with the Nostalgia, Ultra mixtape, issued through his Tumblr blog. Later in the year, he appeared on Tyler, the Creator's Goblin (\"She,\" \"Window\"), Beyoncé's 4 (\"I Miss You\"), and Jay-Z and Kanye West's Watch the Throne (\"No Church in the Wild,\" \"Made in America\"). Def Jam's plan for the release of Nostalgia, Lite — an EP-length version of the mixtape — was scrapped, yet the songs \"Novacane\" (produced by Stewart) and \"Swim Good\" (MIDI Mafia) were released as singles with accompanying videos. The former reached number 17 on Billboard's Hot R&B/Hip-Hop chart. The latter peaked at number 70. By the end of the year, several publications listed Nostalgia, Ultra as one of 2011's best releases. While his association with Def Jam had been strained, Ocean nonetheless proceeded with the making of his official debut album, working beside the likes of Malay, Om'Mas Keith, and Pharrell Williams as fellow producers. The album, Channel Orange, was previewed for journalists at a handful of listening events. Some writers alleged that certain lyrics on the album revealed Ocean's bisexuality. Ocean subsequently published a screen shot of a TextEdit file (entitled \"thank you's\") that included details of a romantic relationship — his first love — with a male. On July 10, six days after the post, Channel Orange was released by Def Jam as a download, while the CD version was issued the following week. Along with featured appearances from Earl Sweatshirt, John Mayer, and André 3000, the album involved material about unrequited love, as well as class and drug dependency — all delivered with Ocean's descriptive storytelling and understated yet expressive vocals. The album would go on to be an all-around success, receiving nearly universal critical acclaim, a spot on the Billboard 200, and a host of Grammy nominations.",
            "youtube_url_1":"https://www.youtube.com/embed/TMfPJT4XjAI",
            "youtube_url_2":"https://www.youtube.com/embed/PmN9rZW0HGo",
            "recommended_album":4,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/310bcbad5e6048493ff198822a54c28c8214f06f"
        },
        {
            "full_name":"Michael Jackson",
            "origin":"Gary, IN",
            "popularity":88,
            "genre":"Pop",
            "spotify_artist_uri":"spotify:artist:3fMbdgg4jU18AjLCKBhRSm",
            "biography": "Michael Joseph Jackson (August 29, 1958 \u2013 June 25, 2009) was an American singer, songwriter, record producer, dancer, and actor. Called the King of Pop, his contributions to music and dance, along with his publicized personal life, made him a global figure in popular culture for over four decades.\nThe eighth child of the Jackson family, he debuted on the professional music scene along with his elder brothers Jackie, Tito, Jermaine, and Marlon as a member of the Jackson 5 in 1964, and began his solo career in 1971. In the early 1980s, Jackson became a dominant figure in popular music. The music videos for his songs, including those of \"Beat It\", \"Billie Jean\", and \"Thriller\", were credited with breaking down racial barriers and with transforming the medium into an art form and promotional tool. The popularity of these videos helped to bring the then- relatively-new television channel MTV to fame. With videos such as \"Black or White\" and \"Scream\", he continued to innovate the medium throughout the 1990s, as well as forging a reputation as a touring solo artist. Through stage and video performances, Jackson popularized a number of complicated dance techniques, such as the robot and the moonwalk, to which he gave the name. His distinctive sound and style has influenced numerous artists of various music genres.\nJackson's 1982 album Thriller is the best-selling album of all time. His other albums, including Off the Wall (1979), Bad (1987), Dangerous (1991), and HIStory (1995), also rank among the world's best-selling albums. Jackson is one of the few artists to have been inducted into the Rock and Roll Hall of Fame twice. He was also inducted into the Songwriters Hall of Fame and the Dance Hall of Fame as the first and only dancer from pop and rock music. His other achievements include multiple Guinness World Records, 13 Grammy Awards, the Grammy Legend Award, the Grammy Lifetime Achievement Award, 26 American Music Awards\u2014more than any other artist\u2014including the \"Artist of the Century\" and \"Artist of the 1980s\", 13 number-one singles in the United States during his solo career,\u2014more than any other male artist in the Hot 100 era\u2014and estimated sales of over 400 million records worldwide. Jackson has won hundreds of awards, making him the most awarded recording artist in the history of popular music. He became the first artist in history to have a top ten single in the Billboard Hot 100 in five different decades when \"Love Never Felt So Good\" reached number nine on May 21, 2014. Jackson traveled the world attending events honoring his humanitarianism, and, in 2000, the Guinness World Records recognized him for supporting 39 charities, more than any other entertainer.\nAspects of Michael Jackson's personal life, including his changing appearance, personal relationships, and behavior, generated controversy. In the mid- 1990s, he was accused of child sexual abuse, but the civil case was settled out of court for an undisclosed amount and no formal charges were brought. In 2005, he was tried and acquitted of further child sexual abuse allegations and several other charges after the jury found him not guilty on all counts. While preparing for his comeback concert series titled This Is It, Jackson died of acute propofol and benzodiazepine intoxication on June 25, 2009, after suffering from cardiac arrest. The Los Angeles County Coroner ruled his death a homicide, and his personal physician Conrad Murray was convicted of involuntary manslaughter. Jackson's death triggered a global outpouring of grief and a live broadcast of his public memorial service was viewed around the world.",          
            "youtube_url_1":"https://www.youtube.com/embed/sOnqjkJTMaA",
            "youtube_url_2":"https://www.youtube.com/embed/h_D3VFfhvs4",
            "recommended_album":5,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/738650ce127e119788a7bca020fbd054b5aa57b5"
        },
        {
            "full_name":"Louis Armstrong",
            "origin":"New Orleans, LA",
            "popularity":74,
            "genre":"Jazz",
            "spotify_artist_uri":"spotify:artist:19eLuQmk9aCobbVDHc6eek",
            "biography":"Louis Armstrong (August 4, 1901 \u2013 July 6, 1971), nicknamed Satchmo or Pops, was an American jazz trumpeter, singer, and an influential figure in jazz music.\nComing to prominence in the 1920s as an \"inventive\" trumpet and cornet player, Armstrong was a foundational influence in jazz, shifting the focus of the music from collective improvisation to solo performance. With his instantly recognizable gravelly voice, Armstrong was also an influential singer, demonstrating great dexterity as an improviser, bending the lyrics and melody of a song for expressive purposes. He was also skilled at scat singing (vocalizing using sounds and syllables instead of actual lyrics).\nRenowned for his charismatic stage presence and voice almost as much as for his trumpet-playing, Armstrong's influence extends well beyond jazz music, and by the end of his career in the 1960s, he was widely regarded as a profound influence on popular music in general. Armstrong was one of the first truly popular African-American entertainers to \"cross over\", whose skin color was secondary to his music in an America that was severely racially divided. He rarely publicly politicized his race, often to the dismay of fellow African- Americans, but took a well- publicized stand for desegregation during the Little Rock Crisis. His artistry and personality allowed him socially acceptable access to the upper echelons of American society that were highly restricted for black men.",
            "youtube_url_1":"https://www.youtube.com/embed/gDrzKBF6gDU",
            "youtube_url_2":"https://www.youtube.com/embed/kmfeKUNDDYs",
            "recommended_album":6,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/7e61be280d4f457b89d563be6b2a11e8ef9e67f3"
        },
        {
            "full_name":"Miles Davis",
            "origin":"Alton, IL",
            "popularity":72,
            "genre":"Jazz",
            "spotify_artist_uri":"spotify:artist:0kbYTNQb4Pb1rPbbaF0pT4",
            "biography":"Miles Dewey Davis III (May 26, 1926 \u2013 September 28, 1991) was an American jazz musician, trumpeter, bandleader, and composer. Widely considered one of the most influential musicians of the 20th century, Miles Davis was, together with his musical groups, at the forefront of several major developments in jazz music, including bebop, cool jazz, hard bop, modal jazz, and jazz fusion.\nIn 2006, Davis was inducted into the Rock and Roll Hall of Fame, which recognized him as \"one of the key figures in the history of jazz\". In 2008, his 1959 album Kind of Blue received its fourth platinum certification from the Recording Industry Association of America (RIAA), for shipments of at least four million copies in the United States. On December 15, 2009, the U.S. House of Representatives passed a symbolic resolution recognizing and commemorating the album Kind of Blue on its 50th anniversary, \"honoring the masterpiece and reaffirming jazz as a national treasure\".",
            "youtube_url_1":"https://www.youtube.com/embed/zqNTltOGh5c",
            "youtube_url_2":"https://www.youtube.com/embed/TLDflhhdPCg",
            "recommended_album":7,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/b1a46506d9efc8a783db76e3d059ce2ffdd33f92"
        },
        {
            "full_name":"Bill Evans",
            "origin":"Plainfield, NJ",
            "popularity":65,
            "genre":"Jazz",
            "spotify_artist_uri":"spotify:artist:4jXfFzeP66Zy67HM2mvIIF",
            "biography":"William John \"Bill\" Evans (pronunciation: /\u02c8\u025bv\u0259ns/, August 16, 1929 \u2013 September 15, 1980) was an American jazz pianist and composer who mostly worked in a trio setting. Evans's use of impressionist harmony, inventive interpretation of traditional jazz repertoire, block chords, and trademark rhythmically independent, \"singing\" melodic lines continue to influence jazz pianists today.\nBorn in Plainfield, New Jersey, he was classically trained, and studied at Southeastern Louisiana University. In 1955, he moved to New York, where he worked with bandleader and theorist George Russell. In 1958, Evans joined Miles Davis's sextet, where he was to have a profound influence. In 1959, the band, then immersed in modal jazz, recorded Kind of Blue, the best-selling jazz album of all time.\nIn late 1959, Evans left the Miles Davis band and began his career as a leader with Scott LaFaro and Paul Motian, a group now regarded as a seminal modern jazz trio. In 1961, ten days after recording the highly acclaimed Sunday at the Village Vanguard and Waltz for Debby, LaFaro died in a car accident. After months of seclusion, Evans re-emerged with a new trio, featuring bassist Chuck Israels.\nIn 1963, Evans recorded Conversations with Myself, an innovative solo album using the unconventional (in jazz solo recordings) technique of overdubbing over himself. In 1966, he met bassist Eddie G\u00f3mez, with whom he would work for eleven years. Several successful albums followed, such as Bill Evans at the Montreux Jazz Festival, Alone and The Bill Evans Album, among others.\nDespite his success as a jazz artist, Evans suffered personal loss and struggled with drug abuse. Both his girlfriend Elaine and his brother Harry committed suicide, and he was a long time user of heroin, and later of cocaine. As a result, his financial stability, personal relationships and musical creativity all steadily declined during his later years.\nMany of his compositions, such as \"Waltz for Debby\", have become standards and have been played and recorded by many artists. Evans was honored with 31 Grammy nominations and seven awards, and was inducted in the Down Beat Jazz Hall of Fame.",
            "youtube_url_1":"https://www.youtube.com/embed/a2LFVWBmoiw",
            "youtube_url_2":"https://www.youtube.com/embed/dH3GSrCmzC8",
            "recommended_album":8,
            "image_url": "https://d3rt1990lpmkn.cloudfront.net/640/47fc8c6072506dede155a28a6e0d096b76ea33a5"
        }]
        api = urlopen(request)
        api_body = api.read().decode("utf-8")
        self.assertEqual(api.getcode(), 200)
        api_data = loads(api_body)

        for artist1, artist2 in zip(api_data, expected_api):
            unmatched_item = set(artist1.items()) ^ set(artist2.items())
            self.assertEqual(len(unmatched_item), 0)

    #----
    #Albums
    #----

    def test_get_albums(self) :
        request = Request(self.url+"api/albums/")
        expected_api = [{"album_artist":1,"album_name":"Encore","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:1kTlYbs28MXw7hwO0NLYif","editors_notes":"Encore closes a six-year period in which Eminem was the most popular, powerful, and controversial rapper in the world. \"Like Toy Soldiers\" looks at the senselessness of Em’s feuds with Source magazine owner Benzino and Murder Inc. crew. Songs like \"Rain Man,\" \"Just Lose It,\" \"My 1st Single,\" and \"A*s Like That\" capture the irreverent insight and trademark mischief that made Slim Shady a star.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/f7be5e8069d250ca6d9991c6c7cf8b21a0922999"},{"album_artist":2,"album_name":"College Dropout","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:3ff2p3LnR6V7m6BinwhNaQ","editors_notes":"Kanye West gained notoriety as a producer-for-hire before The College Dropout shook hip-hop to its core. The mix of styles and subject matter is breathtaking. Pop hits rub up against vulnerable moments. Street anthems mingle with wild humor. And \"Jesus Walks\" challenges beliefs like no other rap song before it. Kanye West attacks the set with confidence and conviction.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/102504bd8952b26857974a3dab5884430245e228"},{"album_artist":3,"album_name":"To Pimp A Butterfly","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:7ycBtnsMtyVbbwTfJwRjSP","editors_notes":"Packed with jazzy, dreamlike production and staggering lyrical work, To Pimp a Butterfly finds Lamar grappling with the weight of his newfound fame. Through the funky menace of \"King Kunta\" he makes blistering reference to the protagonist of Alex Haley’s Roots, while the feverish standout \"The Blacker the Berry\" sees him attack black-on-black crime with singular precision and ferocity.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/d71a94b751b18e4bf7622a05680014c5bb7acb75"},{"album_artist":4,"album_name":"Channel Orange","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:392p3shh2jkxUxY2VHvlH8","editors_notes":"Frank Ocean uses a honeycoated tenor to express what’s on his mind. After opening with falsetto-brushed musings about his first love and spending too much time alone, the soul singer gives us an effervescent, sun-kissed view of life’s simple pleasures ) and a tongue-in-cheek glimpse of what it means to be \"Super Rich Kids\"—featuring Odd Future lyricist Earl Sweatshirt.\"","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/3012f6af84d128b2261b54b40dae836d0102a553"},{"album_artist":5,"album_name":"Bad","release_date":2009,"genre":"rap","spotify_albums_uri":"spotify:album:24TAupSNVWSAHL0R7n71vm","editors_notes":"After Thriller's unprecedented success, Michael Jackson had the impossible task of writing and recording a follow-up. Working under incredible pressure, Jackson expanded on the sonic challenges of Off the Wall and Thriller without losing the radio-ready grooves that had made him an international star. Bad starts with the playful and funky braggadocio of the title track and the upbeat thrill of \"The Way You Make Me Feel.\" Yet \"Man in the Mirror\" pokes fun at Jackson's mythological status, while \"I Just Can't Stop Loving You\" delivers a power ballad with a brainwashing hook worthy of MJ's self-proclaimed (and justified) title of The King of Pop. The sound of the '80s is all over this record, with enhanced beats and funky synths that made it cutting-edge in 1987. \"Just Good Friends\" is a classy duet with Stevie Wonder. However, it's Jackson's fantasies—\"Speed Demon,\" \"Smooth Criminal,\" \"Dirty Diana\"—that push this album over the top.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/74e2e7b7b5c916e785cd3a5fc1b3d117932166ec"},{"album_artist":6,"album_name":"The Essential Louis Armstrong","release_date":2009,"genre":"Jazz","spotify_albums_uri":"spotify:album:2hYLiPQUj7ml70oaoLY8vI","editors_notes":"Even at two discs and 37 tracks, it's difficult to say that this set contains everything that is truly essential from Louis Armstrong's monumental five-decade career. It does, however, do a great job of touching down at key points, and nicely balances Armstrong's various guises as a groundbreaking sideman, soloist, bandleader, singer, and ultimately, American legend, icon, and the very embodiment of the face of jazz. Opening with Armstrong blowing accomplished blues choruses on 1925's \"Sugar Foot Stomp\" while a member of the Fletcher Henderson Orchestra, moving through his revolutionary Hot Five and Seven sessions and his years fronting and leading the Armstrong All-Stars, and concluding with 1968's poignant summation \"What a Wonderful World,\" this lovingly assembled overview sketches a broad outline of perhaps the most important American musician of the 20th century. Armstrong's genius on the trumpet is aptly documented here, but so too is his equally innovative vocal style, which raised scat singing to the level of art, and brought the fluid, bending flow of the horn line into pop vocal phrasing, resulting in definitive versions of \"Ain't Misbehavin',\" \"Black and Blue\" (one of the most subtly important vocal performances in the history of Western pop), \"Lazy River,\" \"Georgia On My Mind,\" \"Stardust,\" \"Blueberry Hill\" (before Fats Domino), \"Mack the Knife\" (before Bobby Darin), and \"What a Wonderful World.\" Serious Armstrong fans and collectors will already have everything here, but if you only have room in your collection for a single Armstrong set, and you want something that touches on the full sweep of his jazz and pop contributions, then this is the one to get.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/403ef41ee127eb73ecb207088a5bd507188a2051"},{"album_artist":7,"album_name":"Kind of Blue","release_date":2009,"genre":"Pop","spotify_albums_uri":"spotify:album:4sb0eMpDn3upAFfyi4q2rw","editors_notes":"The essence of great art is that its power is inexplicable, and in the jazz stratos there's never been anything like this 1959 session. It reigns to this day as the genre's greatest hit and the most coherent album length statement in modern jazz history. Based on scales (modes) rather than chord changes, the five tracks here were recorded in one take without any prior rehearsal, and the cool blue electric spontaneity gives these gossamer lanterns—what pianist Bill Evans called in the liner notes a \"direct deed\"—a freedom that's pure magic. The sax chairs were majestically filled by John Coltrane on tenor and Julian \"Cannonball\" Adderley on alto, both playing at their most ethereal. Longtime Miles bassist Paul Chambers joined stalwart drummer Jimmy Cobb in the rhythm section, and two of the greatest jazz pianists ever, Wynton Kelly (only on \"Freddie Freeloader\") and particularly Evans play brilliantly yet with a smooth,enchanting chill. The result is a collection of modern jazz' greatest moments. For experts and novices alike, \"So What's\" spidery opening exchange between Chambers and Evans has come to symbolize jazz incarnate. Ditto the entirety of \"Freddie Freeloader,\" and the gorgeous and underrated \"Flamingo Sketches\" is Miles and the band at their most tender and introspective. Modern jazz starts here.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/a718805968def67d317cf57d12ad9cb5768f2fd0"},{"album_artist":8,"album_name":"Portrait in Jazz","release_date":2009,"genre":"Jazz","spotify_albums_uri":"spotify:album:7dlYNvbD4QYDL3sSkTCjxi","editors_notes":"This 1959 studio session features Bill Evans with bassist Scott LaFaro and drummer Paul Motian, his earliest important trio and first working group to be recorded. Even at this early stage Evans and his bandmates display a substantial degree of interplay, getting well away from the tradition of the bass and drums playing a totally subservient role to the piano. The pianist's updated arrangements of the seven standards take them into new territory, highlighted by \"Autumn Leaves,\" \"Someday My Prince Will Come,\" and \"Spring Is Here.\" The date is rounded out by two originals, the haunting modal work \"Blue in Green\" made famous on Miles Davis' Kind of Blue (and wrongly credited to Davis as its composer, as Evans insisted upon credit when the original LP of this session was first issued) and the playful, upbeat \"Peri's Scope.\" Previously reissued as a part of Fantasy's Original Jazz Classics series, this Keepnews Collection expanded reissue includes previously unavailable alternate takes of \"Come Rain or Come Shine\" and \"Blue in Green\" that were omitted from the 12-CD The Complete Riverside Recordings boxed set, along with expanded liner notes by Riverside founder/producer Orrin Keepnews.","image_url":"https://d3rt1990lpmkn.cloudfront.net/640/910144cb88b7cda615aa0beb39d5cfd2ee4cb948"}]
        response = urlopen(request)
        response_body = response.read().decode("utf-8")
        self.assertEqual(response.getcode(), 200)
        api_data = loads(response_body)


        for album1, album2 in zip(api_data, expected_api):
            unmatched_item = set(album1.items()) ^ set(album2.items())
            self.assertEqual(len(unmatched_item), 0)


if __name__ == "__main__" :
    main()