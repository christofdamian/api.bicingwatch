from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse

try:
    # Try Python 2.5 and later
    import xml.etree.ElementTree as ET
except ImportError:
    # Older Python 
    import elementtree.ElementTree as ET
    
from bicingwatch.api.models import Station, Ping

def __pings(data):
    pings = ET.Element("pings")
    for ping in data:
        pings.append(ET.Element('ping',
            hour=str(ping["hour"]),
            bikes=str(ping['bikes']),
            free=str(ping['free'])
        ))
        
    return __XmlResponse(pings)
    

def ping_avg(request,station_id):
	return __pings(Ping.avg_by_hour(station_id,[0,1,2,3,4,5,6]))

def ping_avg_weekday(request,station_id):
	return __pings(Ping.avg_by_hour(station_id,[0,1,2,3,4]))

def ping_avg_weekend(request,station_id):
	return __pings(Ping.avg_by_hour(station_id,[5,6]))

def ping_last_24_hours(request,station_id):
    return __pings(Ping.last_24_hours(station_id))

def ping_today(request,station_id):
    pings = ET.Element("pings")
    for ping in Ping.today(station_id):
        pings.append(ET.Element('ping',
            hour=str(ping["time"]),
            bikes=str(ping['bikes']),
            free=str(ping['free'])
        ))
        
    return __XmlResponse(pings)

def stations(request):
    "xml view of stations"
    
    stations = ET.Element("stations")

    for station in Station.objects.all():
        stations.append(ET.Element('station',
            id=str(station.id),
            name=station.name,
            number=str(station.number),
            x=str(station.x),
            y=str(station.y)            
        ))
        
    return __XmlResponse(stations)
            
            
def __XmlResponse(element):
    text = ET.tostring(element, 'UTF-8')
    return HttpResponse(text, mimetype ='text/xml')


