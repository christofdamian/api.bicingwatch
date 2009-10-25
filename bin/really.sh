#!/bin/bash

curl --connect-timeout 30 --silent --insecure --user-agent 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )' https://www.bicing.com/localizaciones/localizaciones.php > ../data/bicing.html &&
./extractkml.py -f ../data/bicing.html -o ../data/bicing.kml &&
iconv -f iso-8859-1  -t utf-8 ../data/bicing.kml -o ../data/bicing.utf8 &&
./parsekml.py -f ../data/bicing.utf8
./addresses.py
