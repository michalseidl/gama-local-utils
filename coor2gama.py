#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts XYZ point list into Gama format (https://www.gnu.org/software/gama/)
Restriction:
- point number X Y Z format only (spaces or comma separated)
- points with constrained coordinates only
- all station id characters makes UPPER
"""

import sys
import lxml.etree as et
from collections import OrderedDict

def parseCoorStdin():
    """
    Reads coors from STDIN
    :return: dataList
    """

    dataList = list()

    for line in sys.stdin:

        # Split line into coordinate data
        if line.find(',') != -1:
            lineData = line.split(',')
        else:
            lineData = line.split()

        lineData[0] = lineData[0].upper()
        dataList.append(lineData)

    dataList.sort(key=lambda x: x[0])

    return dataList

def coor2gamaXml(gamaXmlFilePath):
    """
    Merges coors with existing Gama XML
    :param gamaXmlFilePath:
    :return: gamaXml to STDOUT
    """

    pointList = parseCoorStdin()

    pointSettings = {
        '1P25': {'fix': 'xy', 'adj': 'Z'},
        '2P5': {'fix': 'xy', 'adj': 'Z'},
        '8P5': {'fix': 'xy', 'adj': 'Z'},
        '23': {'fix': 'xy', 'adj': 'Z'},
        '533': {'fix': 'xy', 'adj': 'Z'},
        '536': {'fix': 'xy', 'adj': 'Z'},
        '507': {'fix': 'xy', 'adj': 'Z'},
        '8P9': {'fix': 'xy', 'adj': 'Z'},
        '604': {'fix': 'xy', 'adj': 'Z'},
        '612': {'fix': 'xy', 'adj': 'Z'}
    }

    gamaLocal = et.parse(gamaXmlFilePath)

    NSMAP = {'gama-local': gamaLocal.xpath('namespace-uri(.)')}

    for pointXml in gamaLocal.findall('.//gama-local:point', namespaces=NSMAP):
        for point in pointList:
            if pointXml.get('id') == point[0]:

                # Clear all attributes and set new one
                # BUG lxml clear influence intendation
                # pointXml.clear()
                #pointXml.set('id',point[0])
                if 'fix' in pointXml.attrib:
                    pointXml.attrib.pop('fix')
                if 'adj' in pointXml.attrib:
                    pointXml.attrib.pop('adj')

                pointXml.set('x', point[1])
                pointXml.set('y', point[2])
                pointXml.set('z', point[3])

                # Set settings from pointSettings
                if pointXml.get('id') in pointSettings:
                    if 'fix' in pointSettings[pointXml.get('id')]:
                        pointXml.set('fix', pointSettings[pointXml.get('id')]['fix'])
                    if 'adj' in pointSettings[pointXml.get('id')]:
                        pointXml.set('adj', pointSettings[pointXml.get('id')]['adj'])

                # Set default settings
                else:
                    pointXml.set('adj', 'XYZ')

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

def getGamaXml():
    """
    Generates new Gama XML only with coordinates
    :return: gamaXml to STDOUT
    """

    DOCTYPE = '<?xml version="1.0">'
    XMLNS = 'http://www.gnu.org/software/gama/gama-local'

    # xml header
    gamaLocal = et.Element('gama-local', xmlns=XMLNS)
    network = et.SubElement(gamaLocal, 'network', attrib={'axes-xy':"en"})
    description = et.SubElement(network, 'description')
    description.text = "XML input of points and observation data for the program GNU Gama"
    parameters = et.SubElement(network, 'parameters', attrib={'sigma-act':"aposteriori"})
    pointsObservation = et.SubElement(network, 'points-observations')

    pointList = parseCoorStdin()

    for data in pointList:

        # Point data
        if len(data) > 3:
            point = et.SubElement(pointsObservation, 'point',
                attrib=OrderedDict([('id', data[0].upper()),("x", data[1]),("y", data[2]),("z", data[3]),("adj", 'XYZ')]))

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        gamaXmlFilePath = sys.argv[1]
        coor2gamaXml(gamaXmlFilePath)
    else:
        getGamaXml()