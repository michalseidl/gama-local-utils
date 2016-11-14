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

import gama.xml as gx
from settings import XML_SETTINGS, pointSettings

def __parseCoorStdin():
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

def coor2gamaXml(gamaXmlFilePath, pointSettings):
    """
    Merges coors with existing Gama XML
    :param gamaXmlFilePath:
    :param pointSettings:
    :return: gamaXml to STDOUT
    """

    pointList = __parseCoorStdin()

    gamaLocal = et.parse(gamaXmlFilePath)

    NSMAP = {'gama-local': gamaLocal.xpath('namespace-uri(.)')}

    for pointXml in gamaLocal.findall('.//gama-local:point', namespaces=NSMAP):
        for point in pointList:

            gx.updatePointEl(pointXml, point, pointSettings)

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

def getGamaXml(XML_SETTINGS):
    """
    Generates new Gama XML only with coordinates
    :return: gamaXml to STDOUT
    """

    # Init etree Gama XML object
    gamaLocal = gx.initGamaXml(XML_SETTINGS)

    pointsObservations = et.SubElement(gamaLocal.find('network'), 'points-observations')

    pointList = __parseCoorStdin()

    for data in pointList:

        # Point data
        if len(data) > 3:
            gx.addPointEl(pointsObservations, data)

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        gamaXmlFilePath = sys.argv[1]
        coor2gamaXml(gamaXmlFilePath, pointSettings)
    else:
        getGamaXml(XML_SETTINGS)