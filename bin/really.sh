#!/bin/bash

curl --connect-timeout 30 --silent http://www.bicing.com/localizaciones/localizaciones.php > ../data/bicing.html &&
./extractkml.py -f ../data/bicing.html -o ../data/bicing.kml &&
iconv -f iso-8859-1  -t utf-8 ../data/bicing.kml -o ../data/bicing.utf8 &&
./parsekml.py -f ../data/bicing.utf8
./addresses.py
