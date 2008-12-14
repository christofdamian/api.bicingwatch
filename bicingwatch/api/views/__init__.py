from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page

from bicingwatch.api.models import Station, Ping

@cache_page(60*60)
def index(request):
    return render_to_response('index.html')
 
@cache_page(60*60)
def station_list(request):
    station_list = Station.objects.all().order_by('name')

    return render_to_response('station_list.html', {
        'station_list': station_list
    })

@cache_page(60*60)
def station_map(request):
    station_list = Station.objects.all()
    
    limits = {
            'xmin': 1000,
            'xmax': 0,
            'ymin': 1000,
            'ymax': 0,
              }
    
    for station in station_list:
        if station.x < limits['xmin']:
            limits['xmin'] = station.x
        if station.x > limits['xmax']:
            limits['xmax'] = station.x
        if station.y < limits['ymin']:
            limits['ymin'] = station.y
        if station.y > limits['ymax']:
            limits['ymax'] = station.y
        
    centre = {
              'x': (limits['xmax']+limits['xmin'])/2,
              'y':(limits['ymax']+limits['ymin'])/2
              }
    
    return render_to_response('station_map.html', {
        'limits': limits,
        'centre': centre
        })


def pings(request, station_id):
    
    ping_list = Ping.objects.filter(station = station_id)
    
    return render_to_response('pings.html', {
        'ping_list': ping_list
    })
    
def ping_avg(request, station_id):
    ping_list = Ping.avg_by_hour(station_id)
    
    return render_to_response('ping_avg.html', {
        'ping_list': ping_list
    })

@cache_page(60*60)
def station(request, station_id):
    station = get_object_or_404(Station, id=station_id)
    
    return render_to_response('station.html', {
        'station': station                                        
    })
         

    