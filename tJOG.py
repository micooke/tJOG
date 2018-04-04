#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage : tJOG.py [-h] [-ADL] <inputfile>
    -h : (optional) display help
    -ADL : (optional) set the origin to the city centre of Adelaide (Australia, South Australia)
    
    The output file tJOG_<inputfile> is created, with origin removed/replaced
    
    e.g. tJOG.py -ADL test.gpx

https://github.com/micooke/tJOG

@license: MIT
@copyright: Copyright 2018, Mark Cooke
@author: Mark Cooke (https://github.com/micooke)
"""

import os
import sys
import re

def main():
    url = 'https://github.com/micooke/tJOG'
    usage = 'usage : tJOG.py [-h] [-ADL] <inputfile>'
    inputfile = ''
    outputfile = ''
    latOffset = 0.0
    lonOffset = 0.0
    
    # input sanitisation
    if len(sys.argv) > 1:
        if sys.argv[1] in {'-h','--help'}:
            print(usage)
            return 0
        elif sys.argv[1] in {'-ADL'}:
            latOffset = -34.9286600
            lonOffset = 138.5986300
            inputfile = sys.argv[2]
        elif os.path.isfile(sys.argv[1]):
            inputfile = sys.argv[1]
        else:
            print('error: inputfile "'+sys.argv[1]+'" does not exist')
            return 1
    else:
        print(usage)
        return 1

    # generate the output filename
    outputfile = 'tJOG_'+os.path.splitext(inputfile)[0]+'.gpx'
    
    print('Input file  :', inputfile)
    print('Output file :', outputfile)
    
    # open the input file and read the contents
    with open(inputfile, 'r' ) as f:
        content = f.read()
    
    ## look for the first lat, lon and assume this is the 'origin'
    # generate the lat,lon search pattern
    pattern = re.compile('lat="([^"]+)" lon="([^"]+)"')
    
    # find the first lat,lon instance
    LatLon = pattern.search(content).groups()
    
    # if the string is incomplete, there is no data
    if len(LatLon) != 2:
        print('error : No lat,lon information found in the gpx file')
        return 1
    
    # get the  run origin
    lat0 = float(LatLon[0])
    lon0 = float(LatLon[1])
    
    # replace each lat,lon instance
    iterator = pattern.finditer(content)
    for m in iterator:
        # get the group
        LatLon = m.groups()
        
        # set the origin to lat,lon = 0,0
        lat_ = float(LatLon[0]) - lat0 + latOffset
        lon_ = float(LatLon[1]) - lon0 + lonOffset
        
        # format the lat,lon information to 7 decimal places
        lat_ = "{:.7f}".format(lat_)
        lon_ = "{:.7f}".format(lon_)
        
        # replace the appropriate contents
        content = content.replace(LatLon[0], lat_)
        content = content.replace(LatLon[1], lon_)
    
    # replace the creator details
    s = re.search('creator="([^"]+)"', content).groups()
    content = content.replace(s[0], url)
     
    # write the content to the output file
    with open(outputfile, 'w' ) as f:
        f.write(content)
    
    # normal program return
    return 0

if __name__=="__main__":
    result = main()
    if result > 0:
        sys.exit(result)