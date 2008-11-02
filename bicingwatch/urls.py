from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bicingwatch/', include('bicingwatch.foo.urls')),
    
    (r'^$', 'bicingwatch.api.views.index'),
    (r'^pings/(.*)$', 'bicingwatch.api.views.pings'),
    (r'^ping_avg/(.*)$', 'bicingwatch.api.views.ping_avg'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/(.*)', admin.site.root),
)
