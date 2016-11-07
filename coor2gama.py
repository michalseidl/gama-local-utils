#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts XYZ point list into Gama format (https://www.gnu.org/software/gama/)
Restriction:
- point number X Y Z format only (spaces or comma separated)
- points with constrained coordinates only
"""

import sys
import lxml.etree as et
from collections import OrderedDict

def getGamaXml():

    DOCTYPE = '<?xml version="1.0">'
    XMLNS = 'http://www.gnu.org/software/gama/gama-local'

    # xml header
    gamaLocal = et.Element('gama-local', xmlns=XMLNS)
    network = et.SubElement(gamaLocal, 'network', attrib={'axes-xy':"en"})
    description = et.SubElement(network, 'description')
    description.text = "XML input of points and observation data for the program GNU Gama"
    parameters = et.SubElement(network, 'description', attrib={'sigma-act':"aposteriori"})
    pointsObservation = et.SubElement(network, 'points-observations')


    for line in sys.stdin:

        # Split line into coordinate data
        if line.find(',') != -1:
            data = line.split(',')
        else:
            data = line.split()

        # Point data
        if len(data) > 4:
            point = et.SubElement(pointsObservation, 'point',
                attrib=OrderedDict([('id', data[0]),("x", data[1]),("y", data[2]),("z", data[3]),("adj", 'XYZ')]))

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":
    getGamaXml()