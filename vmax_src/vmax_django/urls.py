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
    url(r'^artistdatabase/$', 'volumemax.views.artistdatabase', name='artistdatabase'),
    url(r'^albumdatabase/$', 'volumemax.views.albumdatabase', name='albumdatabase'),
    
    ################################################################### 
    #
    #   INDIVIDUAL ARTISTS/ALBUMS
    #
    ################################################################### 
    url(r'^artists/(\w+)', 'volumemax.views.artist_view', name='artist_view'),
    url(r'^albums/(\w+)', 'volumemax.views.album_view', name='album_view'),

    ################################################################### 
    #
    #   SEARCH
    #
    ################################################################### 
    url(r'^search/$', 'volumemax.views.search', name='search'),
    url(r'^search/(?P<query>\w+)', 'volumemax.views.search', name='search'),
    #url(r'^results/$', 'volumemax.views.search_results', name='results'),

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
    url(r'^nfl/$', 'volumemax.views.nfl', name='nfl'),
]



if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




