from django.conf.urls.defaults import *
from django.conf import settings

from os.path import dirname


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
		# Example:
		# (r'^bicingwatch/', include('bicingwatch.foo.urls')),

		(r'^$', 'bicingwatch.api.views.index'),
		(r'^station_list$', 'bicingwatch.api.views.station_list'),
		(r'^station_map$', 'bicingwatch.api.views.station_map'),
		(r'^station/(.*)$', 'bicingwatch.api.views.station'),
		(r'^pings/(.*)$', 'bicingwatch.api.views.pings'),
		(r'^ping_avg/(.*)$', 'bicingwatch.api.views.ping_avg'),

		(r'^data/ping_avg/(\d+)$', 'bicingwatch.api.views.data.ping_avg'),
		(r'^data/ping_avg_weekend/(\d+)$', 'bicingwatch.api.views.data.ping_avg_weekend'),
		(r'^data/ping_avg_weekday/(\d+)$', 'bicingwatch.api.views.data.ping_avg_weekday'),
		(r'^data/ping_last_24_hours/(\d+)$', 'bicingwatch.api.views.data.ping_last_24_hours'),
		(r'^data/ping_today/(\d+)$', 'bicingwatch.api.views.data.ping_today'),

		(r'^text/stations$', 'bicingwatch.api.views.text.stations'),
		(r'^text/ping_avg/(\d+)$', 'bicingwatch.api.views.text.ping_avg'),
		(r'^text/ping_avg_weekend/(\d+)$', 'bicingwatch.api.views.text.ping_avg_weekend'),
		(r'^text/ping_avg_weekday/(\d+)$', 'bicingwatch.api.views.text.ping_avg_weekday'),
		(r'^text/ping_last_24_hours/(\d+)$', 'bicingwatch.api.views.text.ping_last_24_hours'),
		(r'^text/ping_today/(\d+)$', 'bicingwatch.api.views.text.ping_today'),

		(r'^xml/stations$', 'bicingwatch.api.views.txml.stations'),
		(r'^xml/ping_avg/(\d+)$', 'bicingwatch.api.views.txml.ping_avg'),
		(r'^xml/ping_avg_weekend/(\d+)$', 'bicingwatch.api.views.txml.ping_avg_weekend'),
		(r'^xml/ping_avg_weekday/(\d+)$', 'bicingwatch.api.views.txml.ping_avg_weekday'),
		(r'^xml/ping_last_24_hours/(\d+)$', 'bicingwatch.api.views.txml.ping_last_24_hours'),
		(r'^xml/ping_today/(\d+)$', 'bicingwatch.api.views.txml.ping_today'),


		(r'^kml/all$', 'bicingwatch.api.views.kml.all'),


		# Uncomment the admin/doc line below and add 'django.contrib.admindocs'
		# to INSTALLED_APPS to enable admin documentation:
		# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

		(r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
		site_media = dirname(__file__)+'/site_media'

		urlpatterns += patterns('',
				(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media+'/images'}),
				(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media+'/js'}),
				(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_media+'/css'}),
		)
