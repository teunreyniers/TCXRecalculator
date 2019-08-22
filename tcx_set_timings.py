#!/usr/bin/env python3

""" Add new timestamps to trackpoints in a TCX file, with an equal amount between each trackpoint """

import argparse
from lxml import etree
import datetime
import math

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
parser.add_argument('starttime')
parser.add_argument('totaltime')

date_str = '%Y-%m-%dT%H:%M:%SZ'
ns1 = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

def set_time(trackpoint, time):
    for child in trackpoint:
        if child.tag == '{:s}Time'.format(ns1):
            child.text = time.strftime(date_str)

if __name__ == '__main__':
    args = parser.parse_args()
    tree = etree.parse(args.input)
    startTime = datetime.datetime.strptime(args.starttime,date_str)
    totaltime = float(args.totaltime)

    trackpoints = tree.findall('//{:s}Trackpoint'.format(ns1))

    trackpointscount = len(trackpoints)
    addseconds = totaltime / trackpointscount
  
    time = startTime
    for trackpoint in trackpoints:
        set_time(trackpoint, time)            
        time = time + datetime.timedelta(0, addseconds)

    lap = tree.find('//{:s}Lap'.format(ns1))
    lap.attrib["StartTime"] = startTime.strftime(date_str)
    for child in lap:
        if child.tag == '{:s}TotalTimeSeconds'.format(ns1):
            child.text = '{:.1f}'.format(totaltime)

    tree.write(args.output, xml_declaration=True, encoding='utf-8')
    print('Wrote output XML to', args.output)
