#!/bin/bash

rsync -n --exclude "settings.*" --exclude "*.py[co]" -avz bin bicingwatch www@batgirl.krass.com:bw.damian.net/
