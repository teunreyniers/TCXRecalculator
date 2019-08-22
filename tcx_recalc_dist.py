#!/usr/bin/env python3

""" Recalculate the distance in a TCX file """

import argparse
from lxml import etree
import math

parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')

ns1 = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
ns2 = '{http://www.garmin.com/xmlschemas/ActivityExtension/v2}'

def get_coordinates(trackpoint):
    for child in trackpoint:
        if child.tag == '{:s}Position'.format(ns1):
            for subchild in child:
                if subchild.tag == '{:s}LatitudeDegrees'.format(ns1):
                    lat = float(subchild.text)
                if subchild.tag == '{:s}LongitudeDegrees'.format(ns1):
                    lng = float(subchild.text)
            return (lat, lng)


def set_distance(trackpoint, distance):
    for child in trackpoint:
        if child.tag == '{:s}DistanceMeters'.format(ns1):
            child.text = distance


def calculateDistance(c1, c2):
    R = 6371e3
    p1 = c1[0] / 180 * math.pi
    p2 = c2[0] / 180 * math.pi
    Dp = p2 - p1
    Dl = (c2[1] - c1[1]) / 180 * math.pi
    a = math.sin(Dp/2) * math.sin(Dp/2) + math.cos(p1) * math.cos(p2) * math.sin(Dl/2) * math.sin(Dl/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

if __name__ == '__main__':
    args = parser.parse_args()
    tree = etree.parse(args.input)

    laps = tree.find('//{:s}Lap'.format(ns1))
    trackpoints = tree.findall('//{:s}Trackpoint'.format(ns1))
  
    preLoc = None
    totalDistance = 0
    for trackpoint in trackpoints:
        loc = get_coordinates(trackpoint)
        if preLoc == None:
            set_distance(trackpoint, "0.0")
        else:            
            d = calculateDistance(preLoc, loc)
            totalDistance += d
            print(f'{preLoc} -> {loc} = {d}')
            set_distance(trackpoint, str(totalDistance))
            
        preLoc = loc

    for child in laps:
        if child.tag == '{:s}DistanceMeters'.format(ns1):
            child.text = '{:.4f}'.format(totalDistance)

    tree.write(args.output, xml_declaration=True, encoding='utf-8')
    print(f'Total distance: {totalDistance}')
    print('Wrote output XML to', args.output)
