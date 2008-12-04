from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.cache import cache_page

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
                "values": bikes,
                "text": "bikes",
                "dot-size": 3,
                },
              {
                "type": "line_dot",
                "colour": "#00ff00",
                "values": free,
                "text": "free places",
                "dot-size": 3,
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

@cache_page(60*60*24)        
def ping_avg(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4,5,6])

@cache_page(60*60*24)        
def ping_avg_weekday(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4])

@cache_page(60*60*24)        
def ping_avg_weekend(request,station_id):
    return __ping_avg(request,station_id,[5,6])

def ping_last_24_hours(request,station_id):
    "json view for last 24 hours"

    bikes = []
    free = []
    hours = []
    for ping in Ping.last_24_hours(station_id):
        bikes.append(int(ping['bikes']))
        free.append(int(ping['free']))
        hours.append(str(ping['hour']))
                     
    elements = [
                {
                "colour": "#ff0000",
                "type": "line_dot",
                "values": bikes,
                "text": "bikes",
                "dot-size": 3,
                },
              {
                "type": "line_dot",
                "colour": "#00ff00",
                "values": free,
                "text": "free places",
                "dot-size": 3,
                },
               ]
   
    graph = {
             "title": { "text": "Average By Hour" },  
             "elements": elements,
             "y_axis": {
                        "min": 0,
                        "max": 39,
                        "steps": 3
                        },
            "x_axis": {
                       "labels":  { "labels" : hours },
                       }
            }
    
    return HttpResponse(json.write(graph))

def ping_today(request,station_id):
    "json view for today"

    bikes = []
    free = []
    for ping in Ping.today(station_id):
        bikes.append(int(ping['bikes']))
        free.append(int(ping['free']))
                     
    elements = [
                {
                "colour": "#ff0000",
                "type": "line_dot",
                "values": bikes,
                "text": "bikes",
                "dot-size": 3,
                },
              {
                "type": "line_dot",
                "colour": "#00ff00",
                "values": free,
                "text": "free places",
                "dot-size": 3,
                },
               ]
   
    graph = {
             "title": { "text": "Average By Hour" },  
             "elements": elements,
             "y_axis": {
                        "min": 0,
                        "max": 39,
                        "steps": 3
                        },
            "x_axis": {
                       "labels":  { "labels" : [str(i) for i in range(0,24)] },
                       }
            }
    
    return HttpResponse(json.write(graph))
