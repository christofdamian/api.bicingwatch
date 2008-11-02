from django.shortcuts import render_to_response

from bicingwatch.api.models import Station

def index(request):
    station_list = Station.objects.all().order_by('name')

    return render_to_response('index.html', {
        'station_list': station_list
    })
