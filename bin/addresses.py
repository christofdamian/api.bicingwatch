#!/bin/env python

'''find missing addresses'''

import sys

# get the django model
sys.path.append("../bicingwatch")
from django.core.management import setup_environ
import settings
setup_environ(settings)
from bicingwatch.api.models import Station
import os

def update_address(station):
    ''' fetch geoloc from google and update database '''
    import urllib
    import simplejson as json

    url = "http://maps.google.com/maps/geo?ll=%f,%f&output=json" % (
        station.y, station.x
        )
    f = urllib.urlopen(url) 
    geo = json.loads(f.read())
    
    if geo['Status']['code'] != 200:
        print "code"+str(geo['Status']['code'])
        return
     
    station.address = unicode(geo['Placemark'][0]['address'],'iso-8859-1')
    station.save()
        
def main():
    import time

    for station in Station.objects.filter(address = '')[:4]:
        update_address(station)
        #print "updated %d '%s' address to '%s'" % ( 
        #                                           station.number,
        #                                           station.name,
        #                                           station.address
        #                                           )

        time.sleep(15)
        
if __name__ == "__main__":
    main()
