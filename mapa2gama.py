#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts MAPA2 format into Gama format (https://www.gnu.org/software/gama/)
Restriction:
- data type 1 only
- sloupe distance only
- first telescope position only
- all station id characters makes UPPER

"""

import sys, math
import lxml.etree as et
from collections import OrderedDict

def getStDev(type, data):

    stDevDir = 60.
    stDevDist = (15., 2.)
    stDevZ = 60.


    if type == 'direction':
        stDev = str(round(stDevDir / (float(data[1])/100.)))
    elif type == 's-distance':
        stDev = str(round(stDevDist[0] + stDevDist[1]*float(data[1])/1000))
    elif type == 'z-angle':
        stDev = str(round(stDevZ / (float(data[1]) / 100.)))

    return stDev

def getGamaXml():

    XML_SETTINGS = {
        'XMLNS': 'http://www.gnu.org/software/gama/gama-local',
        'network': {
            'axes-xy': "en"
        },
        'description': "XML input of points and observation data for the program GNU Gama",
        'parameters': {
            'sigma-apr': "10",
            'conf-pr': "0.9999999",
            'tol-abs': "1000",
            'sigma-act': "aposteriori",
            'update-constrained-coordinates': "no"
        }
    }

    DOCTYPE = '<?xml version="1.0">'

    # xml header
    gamaLocal = et.Element('gama-local', xmlns=XML_SETTINGS['XMLNS'])
    network = et.SubElement(gamaLocal, 'network', attrib=XML_SETTINGS['network'])
    description = et.SubElement(network, 'description')
    description.text = XML_SETTINGS['description']
    parameters = et.SubElement(network, 'parameters', attrib=XML_SETTINGS['parameters'])
    pointsObservation = et.SubElement(network, 'points-observations')

    ro = 200/math.pi
    pointSet = set()
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
        et.SubElement(pointsObservation, 'point',
            attrib=OrderedDict([('id', point.upper()), ('adj', 'xyz')]))

    for data in dataList:

        obs = et.SubElement(pointsObservation, 'obs',
            attrib=OrderedDict([('from', data[0]),('from_dh', data[1])]))

        for meas in data[2]:

            direction = et.SubElement(obs, 'direction',
                attrib=OrderedDict([('to', meas[0]),('val', meas[3]),('stdev', getStDev('direction',meas))]))

        #            distance = et.SubElement(obs, 'distance',
        #                attrib=OrderedDict([('to', data[0]),
        #                    ("val", str(float(data[1])*math.sin(float(data[4])/ro))),("stdev", '10')]))


            s_distance = et.SubElement(obs, 's-distance',
                attrib=OrderedDict([('to', meas[0]),("to_dh", meas[2]),
                    ("val", meas[1]),("stdev", getStDev('s-distance',meas))]))

            z_angle = et.SubElement(obs, 'z-angle',
                attrib=OrderedDict([('to', meas[0]),("to_dh", meas[2]),
                    ("val", meas[4]),("stdev", getStDev('z-angle',meas))]))


    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":
    getGamaXml()