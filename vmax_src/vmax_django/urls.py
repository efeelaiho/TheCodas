"""vmax_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    ################################################################### 
    #
    #   MAIN NAVBAR
    #
    ################################################################### 
	url(r'^$', 'volumemax.views.home', name='home'),
	url(r'^about/', 'volumemax.views.about', name='about'),
	url(r'^artists/$', 'volumemax.views.artists', name='artists'),
    url(r'^albums/$', 'volumemax.views.albums', name='albums'),
    url(r'^database/$', 'volumemax.views.database', name='database'),
    
    ################################################################### 
    #
    #   ARTISTS
    #
    ################################################################### 
    url(r'^eminem/', 'volumemax.views.eminem', name='eminem'),
    url(r'^artist/([0-9]+)/$', 'volumemax.views.artist_view', name='artist_view'),
    url(r'^kanye_west/', 'volumemax.views.kanyewest', name='kanye_west'),
    url(r'^michael_jackson/', 'volumemax.views.michael', name='michael_jackson'),
    ################################################################### 
    #
    #   ALBUMS
    #
    ################################################################### 
    url(r'^encore/', 'volumemax.views.encore', name='encore'),
    url(r'^bad/', 'volumemax.views.bad', name='bad'),
    url(r'^college/', 'volumemax.views.college', name='college'),
    url(r'^album/([0-9]+)/$', 'volumemax.views.album_view', name='album_view'),

	###################################################################    
    #
    #   ADMIN
    #
    ################################################################### 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/artists/$', 'volumemax.views.artist_list', name='api'),    
    url(r'^api/albums/$', 'volumemax.views.album_list', name='api'),    
    url(r'^api/artists/(?P<pk>[0-9]+)/$', 'volumemax.views.artist_detail', name='api'),
    url(r'^api/albums/(?P<pk>[0-9]+)/$', 'volumemax.views.album_detail', name='api'),
]



if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




