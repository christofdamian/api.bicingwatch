#!/bin/bash

./extractkml.py -f ../data/bicing.html -o ../data/bicing.kml
iconv -f iso-8859-1  -t utf-8 ../data/bicing.kml -o ../data/bicing.utf8
./parsekml.py -f ../data/bicing.utf8
