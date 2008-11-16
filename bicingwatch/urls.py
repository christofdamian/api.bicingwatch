from django.conf.urls.defaults import *
from django.conf import settings

from os.path import dirname


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bicingwatch/', include('bicingwatch.foo.urls')),
    
    (r'^$', 'bicingwatch.api.views.index'),
    (r'^station/(.*)$', 'bicingwatch.api.views.station'),
    (r'^pings/(.*)$', 'bicingwatch.api.views.pings'),
    (r'^ping_avg/(.*)$', 'bicingwatch.api.views.ping_avg'),

    (r'^data/ping_avg/(.*)$', 'bicingwatch.api.views.data.ping_avg'),
    (r'^data/ping_avg_weekend/(.*)$', 'bicingwatch.api.views.data.ping_avg_weekend'),
    (r'^data/ping_avg_weekday/(.*)$', 'bicingwatch.api.views.data.ping_avg_weekday'),
    
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
