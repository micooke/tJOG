#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
usage : tJOG.py <inputfile> <outputfile>

https://github.com/micooke/tJOG

Author: Mark Cooke
"""

import os
import sys, getopt
import gpxpy
#import mplleaflet
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.interpolate import interp1d
#import seawater as sw
#import re # regular expressions
from pandas import DataFrame

def gpx_import:


def main():
    inputfile = ''
    outputfile = ''
    if len(sys.argv) == 3:
        inputfile = sys.argv[1]
        outputfile = sys.argv[2]
    else:
        print('usage : tJOG.py <inputfile> <outputfile>')
        sys.exit(1)

    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
   
       # open the source file
    gpx = gpxpy.parse(open(inputfile))
    #!head -n 18 example_trk.gpx
    TPE = gpx.tracks[0].segments[0].points[0].extensions[0]
    
    # gather the TrackPointExtension field names
    data_fieldnames = ['lat','lon','ele','time','speed']
    for child in TPE:
      data_fieldnames.append(re.sub('[^}]+}','',child.tag))
    
    # parse all the data
    data = []
    segment = gpx.tracks[0].segments[0]
    for point_idx, point in enumerate(segment.points):
        point_data = [point.latitude, point.longitude, point.elevation, point.time, segment.get_speed(point_idx)]
        for child in point.extensions[0]:
            point_data.append(float(child.text))
        data.append(point_data)
    
    # create the DataFrame object
    df = DataFrame(data, columns=data_fieldnames)
    
    # assume cadence < 100 indicates single foot cadence (i.e. it needs to be doubled)
    if 'cad' in df.columns:
      if np.median(df['cad'][0:int(len(df['cad'])/2)]) < 100:
        df['cad'] *= 2 
    
    # display some of the table data
    df.head()
    
    # remove the origin
    lon0 = df['lon'][0]
    lat0 = df['lat'][0]
    
    df['lon'] -= lon0
    df['lat'] -= lat0
    
    # display more data
    df.head()
    
    # save to the output file
    
    return 0


if __name__=="__main__":
    sys.exit(main())
