from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
import json
    
from bicingwatch.api.models import Station, Ping
    
    
def ping_avg(request,station_id):
    "json view for avg_by hour"

    bikes = []
    free = []
    for ping in Ping.avg_by_hour(station_id):
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
