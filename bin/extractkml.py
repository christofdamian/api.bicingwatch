#!/bin/env python

'''read bicing html file and extract the kml'''

import sys
import re
from optparse import OptionParser

def parse_options():
    '''parse command line options'''
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="html", default="bicing.html",
              help="read html from HTML")
    parser.add_option("-o", "--output", dest="kml", default="bicing.kml",
              help="write kml to KML")
    
    (options, args) = parser.parse_args()
    
    return options

def read_html(filename):
    '''read and return html file'''
    try: 
        html_file = open(filename, 'r')
        content = html_file.read()
        html_file.close()
    except IOError:
        print "can't read html file '%s'" % filename
        sys.exit()
        
    return content

def write_kml(filename, content):
    '''write content to kml file'''
    try:
        kml_file = open(filename, 'w')
        kml_file.write(content)
        kml_file.close()
    except IOError:
        print "can't write kml file '%s'" % filename
        sys.exit()


def main():
    '''main script'''
    options = parse_options()
    html = read_html(options.html)    
    
    regex = re.compile(r"exml.parseString\('(.*?)'\);", re.DOTALL | re.UNICODE)
    match = regex.search(html)
    if match == None :
        print "kml string not found in file"
        sys.exit()
    
    write_kml(options.kml, match.group(1))

if __name__ == "__main__":
    main()
