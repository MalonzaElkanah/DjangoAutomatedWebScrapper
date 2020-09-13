from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.index, name = 'data-index'),
	url(r'^create-site', views.create_site, name = 'create-site'),
	url(r'^update-site', views.update_site, name = 'update-site'),
	url(r'^scrap-site', views.scrap_site, name = 'scrap-site'),
	url(r'^delete-site/(?P<site_id>[0-9]+)/', views.delete_site, name = 'delete-site'),	
	url(r'^delete-scrapper/(?P<scrapper_id>[0-9]+)/', views.delete_scrapper, name = 'delete-scrapper'),
	url(r'^delete-run/(?P<run_id>[0-9]+)/', views.delete_run, name = 'delete-run'),	
	url(r'^check-run/(?P<run_id>[0-9]+)/', views.check_run, name = 'check-run'),	
]
