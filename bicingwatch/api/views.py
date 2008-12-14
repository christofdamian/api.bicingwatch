from django.shortcuts import render_to_response

from bicingwatch.api.models import Station, Ping

def index(request):
    station_list = Station.objects.all().order_by('name')

    return render_to_response('index.html', {
        'station_list': station_list
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
     

    