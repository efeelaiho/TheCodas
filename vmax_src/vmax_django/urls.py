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
	url(r'^artists/', 'volumemax.views.artists', name='artists'),
    url(r'^albums/', 'volumemax.views.albums', name='albums'),
    ################################################################### 
    #
    #   ARTISTS
    #
    ################################################################### 
    url(r'^eminem/', 'volumemax.views.eminem', name='eminem'),
    url(r'^kanyewest/', 'volumemax.views.kanyewest', name='kanyewest'),
    url(r'^michael/', 'volumemax.views.michael', name='michael'),
    ################################################################### 
    #
    #   ALBUMS
    #
    ################################################################### 
    url(r'^encore/', 'volumemax.views.encore', name='encore'),
    url(r'^bad/', 'volumemax.views.bad', name='bad'),
    url(r'^college/', 'volumemax.views.college', name='college'),    
	###################################################################    
    #
    #   ADMIN
    #
    ################################################################### 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^artist_list/', 'volumemax.views.artist_list', name='api'),    
    url(r'^album_list/', 'volumemax.views.album_list', name='api'),    

]



if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




