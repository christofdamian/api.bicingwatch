from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.cache import cache_page
from django.core.cache import cache

import simplejson as json
    
from bicingwatch.api.models import Station, Ping

def ping_max(station_id):
    cache_key = 'ping_max_'+station_id
    max = cache.get(cache_key)
    if max == None:
        max = Ping.max(station_id)
        cache.set(cache_key,max,60*60*24)
    return max

def __ping_avg(request,station_id,days):
    "json view for avg_by hour"

    max = ping_max(station_id)

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
                        "max": max['max'],
                        "steps": 3
                        }   
             }
    
    
    return HttpResponse(json.dumps(graph))



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
    
    return HttpResponse(json.dumps(graph))

def ping_today(request,station_id):
    "json view for today"

    max = ping_max(station_id)

    bikes = []
    free = []
    broken = []
    for ping in Ping.today(station_id):
        bikes.append({
                     "y": float(ping['bikes']),
                     "x": float(ping['time'])
                     })
        free.append({
                     "y": float(ping['free']),
                     "x": float(ping['time'])
                     })
        broken.append({
                       "y": max['max']-float(ping['bikes'])-float(ping['free']),
                       "x": float(ping['time'])
                       })
                     
    elements = [
                {
                "colour": "#ff0000",
                "type": "scatter_line",
                "values": bikes,
                "text": "bikes",
                "dot-size": 1,
                },
              {
                "type": "scatter_line",
                "colour": "#00ff00",
                "values": free,
                "text": "free places",
                "dot-size": 1,
                },
              {
                "type": "scatter_line",
                "colour": "#000000",
                "values": broken,
                "text": "maybe broken",
                "dot-size": 1,
                },
               ]
   
    graph = {
             "title": { "text": "Average By Half Hour" },  
             "elements": elements,
             "y_axis": {
                        "min": 0,
                        "max": max['max'],
                        "steps": 3
                        },
            "x_axis": {
                       "min": 0,
                       "max": 24
                       }
            }
    
    return HttpResponse(json.dumps(graph))

def stations(request):
    "json view for stations"

    stations = []
    i = 0
    for station in Station.objects.all():
        stations.append({
                         "id": station.id,
                         "number": station.number,
                         "name": station.name,
                         "x": station.x,
                         "y": station.y,
                         })
        i = i+1
        if (i>10):
            break
        
    
    return HttpResponse("var stations = "+json.dumps(stations)+";")
