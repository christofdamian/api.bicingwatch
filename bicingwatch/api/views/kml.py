from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.cache import cache_page
from django.http import HttpResponseRedirect,HttpResponse

from bicingwatch.api.models import Station, Ping

@cache_page(60*60)
def all(request):
    "kml view of all stations"
    
    station_list = Station.objects.all()
        
    return render_to_response('map.kml', {
        'station_list': station_list
        },
        mimetype = 'application/vnd.google-earth.kml+xml'
    )
