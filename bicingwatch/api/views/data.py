from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
import json
    
from bicingwatch.api.models import Station, Ping
        
def __ping_avg(request,station_id,days):
    "json view for avg_by hour"

    bikes = []
    free = []
    for ping in Ping.avg_by_hour(station_id,days):
        bikes.append(int(ping['bikes']))
        free.append(int(ping['free']))
    
    
    elements = [
                {
                "colour": "#ff0000",
                "type": "line_dot",
                "values": bikes
                },
              {
                "type": "line_dot",
                "colour": "#00ff00",
                "values": free
                },
               ]
   
    graph = {
             "title": { "text": "Average By Hour" },  
             "elements": elements,
             "y_axis": {
                        "min": 0,
                        "max": 39,
                        "steps": 3
                        }   
             }
    
    
    return HttpResponse(json.write(graph))

def ping_avg(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4,5,6])

def ping_avg_weekday(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4])

def ping_avg_weekend(request,station_id):
    return __ping_avg(request,station_id,[5,6])

