#!/bin/env python

'''parse bicing kml file and write it to the database'''

import sys
from optparse import OptionParser
import re
import datetime

try:
    # Try Python 2.5 and later
    import xml.etree.ElementTree as ET
except ImportError:
    # Older Python 
    import elementtree.ElementTree as ET


sys.path.append("../bicingwatch")


from django.core.management import setup_environ
import settings
setup_environ(settings)
from bicingwatch.api import models

def parse_options():
    '''parse command line options'''
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="kml", default="bicing.kml",
              help="read kml from KML")
    
    (options, args) = parser.parse_args()
    
    return options

def handle_placemark(placemark, timestamp, number = None, namespace = ''):
    '''handle one placemark and write ping and station to database'''
    descregex = re.compile(r'''
        <div.*?>
            <div.*?>(.*?)</div>
            <div.*?>.*?</div>
            <div.*?>([-\d]+)<br\s*/>([-\d]+)''', 
        re.UNICODE | re.VERBOSE)

    
    description = placemark.findtext('{%s}description' % namespace)
    style = placemark.findtext('{%s}styleUrl' % namespace)
    coord = placemark.findtext(
        '{%s}Point/{%s}coordinates' % (namespace, namespace)
    )
        
    if style.find("green") >= 0:
        status = models.Ping.STATUS_GREEN
    else:
        status = models.Ping.STATUS_RED 
        
    match = re.search(descregex, description)
    
    coord = coord.replace('?','')
    
    # fix comma problem
    p = re.compile('^(\d+),(\d+),(\d+),(\d+),(\d+)$')
    coord = p.sub(r'\1.\2,\3.\4,\5', coord)        
        
    [coord_x, coord_y, ignore] =  coord.split(',', 2)
        
    try:
        station = models.Station.objects.get(x = coord_x, y = coord_y)
    except models.Station.DoesNotExist:
        station = models.Station()
        station.x = coord_x
        station.y = coord_y
        station.created = timestamp

    station.name = match.group(1).replace("\\'","'")
    
    m = re.match('^(\d+)\s+-\s+(.*)', station.name, re.UNICODE)
    if m is not None:
        number = m.group(1)
        station.name = m.group(2)
    
    station.number = number
    station.save()

    ping = models.Ping()
    ping.station = station
    ping.bikes = match.group(2)
    ping.free = match.group(3)
    ping.status = status
    ping.timestamp = timestamp
    ping.save()


def main():
    '''main script function'''
    
    options = parse_options()
    
    tree = ET.parse(options.kml)
    kml = tree.getroot()
    
    timestamp = datetime.datetime.now()
    
    namespace = 'http://earth.google.es/kml/2.0'
    number = 0
    for placemark in kml.findall(
        '{%s}Document/{%s}Placemark' % (namespace, namespace)
        ):
        number += 1
        handle_placemark(placemark, timestamp, number, namespace)

if __name__ == "__main__":
    main()
   