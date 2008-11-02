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

    