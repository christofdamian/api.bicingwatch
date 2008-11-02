#!/bin/env python

import xml
import sys
from xml.dom.ext.reader import Sax2
from optparse import OptionParser
import xml.etree.ElementTree as ET
import re
import string
import datetime

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

def handle_placemark(placemark, ns = ''):
    descregex = re.compile("<div.*?><div.*?>(.*?)</div><div.*?>.*?</div><div.*?>(\d+)<br />(\d+)", 
                        re.UNICODE)

    
    description = placemark.findtext('{%s}description' % ns)
    style = placemark.findtext('{%s}styleUrl' % ns)
    coord = placemark.findtext('{%s}Point/{%s}coordinates' % (ns,ns))
    
    if style.find("green") >= 0:
        status = 'G'
    else:
        status = 'R' 
    
    match = re.search(descregex, description)
    
    [x, y, ignore] =  coord.split(',',2)
    
    try:
        station = models.Station.objects.get(x = x, y = y)
    except models.Station.DoesNotExist:
        station = models.Station()
        station.x = x
        station.y = y
        
    station.name = match.group(1).replace("\\'","'")
    station.save()

    ping = models.Ping()
    ping.station = station
    ping.free = match.group(2)
    ping.bikes = match.group(3)
    ping.status = status
    ping.timestamp = datetime.datetime.now()
    ping.save()


def main():
    '''main script function'''
    
    options = parse_options()
    
    tree=ET.parse(options.kml)
    kml=tree.getroot()

    ns = 'http://earth.google.es/kml/2.0'
    for placemark in kml.findall('{%s}Document/{%s}Placemark' % (ns,ns)):
        handle_placemark(placemark, ns)

main()   