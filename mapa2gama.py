#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts MAPA2 format into Gama format (https://www.gnu.org/software/gama/)
Restriction:
- data type 1 only - polar data
- sloupe distance only
- first telescope position only
- all station id characters will be changed UPPER

"""

import sys
import lxml.etree as et

import gama.xml as gx
from settings import XML_SETTINGS

def getGamaXml(XML_SETTINGS):

    # Init etree Gama XML object
    gamaLocal = gx.initGamaXml(XML_SETTINGS)

    # Add pointObservation element
    pointsObservations = et.SubElement(gamaLocal.find('network'), 'points-observations')

    # Point ids
    pointSet = set()
    # Measured data
    dataList = list()

    for line in sys.stdin:

        # Detect type of block data
        data = line.split()

        # Remove point code if exists
        if data[-1].find('*') != -1:
            data.pop(-1)

        # Station data
        if line.startswith('1 ') and len(data) == 3:

            pointSet.add(data[1])
            dataList.append([data[1], data[2], list()])

        # Measured data
        if (len(data) == 6 and data[1] == 2) or len(data) == 5:

            # If type of distance specified, reduce to five elements
            if len(data) == 6:
                data.pop(1)

            pointSet.add(data[0])
            dataList[-1][2].append(data)

            # End of orientation
            # if -1
            # Measured data
            # if -1 and data
            # End of station data
            # if /
            # End of file
            # if -2

    pointList = list(pointSet)
    pointList.sort(key=lambda x: x[0])

    for point in pointList:
        point = gx.addPointEl(pointsObservations,point)

    for data in dataList:
        obs = gx.addObsEl(pointsObservations, data)

        for meas in data[2]:
            direction = gx.addDirEl(obs, meas)
            s_distance = gx.addSdistEl(obs, meas)
            z_angle = gx.addZangleEl(obs, meas)

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":
    getGamaXml(XML_SETTINGS)