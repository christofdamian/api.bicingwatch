from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect,HttpResponse
import json
import csv 
import UnicodeCSV

from bicingwatch.api.models import Station, Ping
        
def __ping_avg(request,station_id,days):
    "csv view for avg_by hour"

    response = HttpResponse(mimetype='text/csv')
    writer = csv.writer(response)

    writer.writerow(['bikes','free'])
    for ping in Ping.avg_by_hour(station_id,days):
        writer.writerow([ping['bikes'],ping['free']])
  
    return response

def ping_avg(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4,5,6])

def ping_avg_weekday(request,station_id):
    return __ping_avg(request,station_id,[0,1,2,3,4])

def ping_avg_weekend(request,station_id):
    return __ping_avg(request,station_id,[5,6])

def ping_last_24_hours(request,station_id):
    "csv view for last 24 hours"

    response = HttpResponse(mimetype='text/csv')
    writer = csv.writer(response)
    
    writer.writerow(['bikes','free','hour'])
    for ping in Ping.last_24_hours(station_id):
        writer.writerow([ping['bikes'],ping['free'],ping['hour']])
  
    return response

def ping_today(request,station_id):
    "csv view for today"

    response = HttpResponse(mimetype='text/csv')
    writer = csv.writer(response)
    
    writer.writerow(['bikes','free'])
    for ping in Ping.today(station_id):
        writer.writerow([ping['bikes'],ping['free']])
  
    return response

def stations(request):
    "stations"

    text = '"id","name","number","x","y"'+"\r\n"
    
    # couldn't get this one to work with the csv writer and python2.4 so far
    for station in Station.objects.all():
        text += ('"'+str(station.id)+'",'+
                 '"'+station.name+'",'+
                 '"'+str(station.number)+'",'+
                 '"'+str(station.x)+'",'+
                 '"'+str(station.y)+'"'
                 "\r\n")
  
    return HttpResponse(text, mimetype ='text/csv')
    
