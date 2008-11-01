#!/bin/env python

import xml
import sys
from xml.dom.ext.reader import Sax2
from optparse import OptionParser
import xml.etree.ElementTree as ET
import re
import string

#from django.core.management import setup_environ
#import settings
#setup_environ(settings)
#from foo import models

def parse_options():
    '''parse command line options'''
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="kml", default="bicing.kml",
              help="read kml from KML")
    
    (options, args) = parser.parse_args()
    
    return options

def handle_placemark(placemark):
    description = placemark.findtext('{%s}description' % ns)
    style = placemark.findtext('{%s}styleUrl' % ns)
    coord = placemark.findtext('{%s}Point/{%s}coordinates' % (ns,ns))
    
    if style.find("green") >= 0:
        print "green"
    else:
        print "red"
    
    match = re.search(descregex, description)
    print match.group(1)
    print match.group(2)
    print match.group(3)

def main():
    '''main script function'''
    
    options = parse_options()
    
    tree=ET.parse(options.kml)
    kml=tree.getroot()

    descregex = re.compile("<div.*?><div.*?>(.*?)</div><div.*?>.*?</div><div.*?>(\d+)<br />(\d+)", 
                           re.UNICODE)

    ns = 'http://earth.google.es/kml/2.0'
    for placemark in kml.findall('{%s}Document/{%s}Placemark' % (ns,ns)):

main()   