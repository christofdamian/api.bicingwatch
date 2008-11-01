#!/bin/env python

import re

f = open('../data/bicing.html','r')
html = f.read()
f.close()


regex = re.compile(r"exml.parseString\('(.*?)'\);",re.DOTALL | re.UNICODE)
match = regex.search(html)

f = open('../data/bicing.kml','w')
f.write(match.group(1))
f.close()
