#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts MAPA2 format into Gama format (https://www.gnu.org/software/gama/)
Restriction:
- data type 1 only
- sloupe distance only
- first telescope position only
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

        # Detect type of block data
        data = line.split()

        # Remove point code if exists
        if data[-1].find('*') != -1:
            data.pop(-1)

        # Station data
        if line.startswith('1 ') and len(data) == 3:
            obs = et.SubElement(pointsObservation, 'obs', attrib={'from': data[1]})
            ih = data[2]

        # Orientation data
        if (len(data) == 6 and data[1] == 2) or len(data) == 5:

            # If type of distance specified, reduce to five elements
            if len(data) == 6:
                data.pop(1)

            direction = et.SubElement(obs, 'direction',
                attrib=OrderedDict([('to', data[0]),("val", data[3]),("stdev", '10')]))
            s_distance = et.SubElement(obs, 's-distance',
                attrib=OrderedDict([('to', data[0]),("from_dh", ih),("to_dh", data[2]),
                    ("val", data[1]),("stdev", '10')]))
            z_angle = et.SubElement(obs, 'z-angle',
                                   attrib=OrderedDict([('to', data[0]),("val", data[4]),("stdev", '10')]))
        # End of orientation
        # if -1
        # Measured data
        # if -1 and data
        # End of station data
        # if /
        # End of file
        # if -2

    xml = et.tostring(gamaLocal, pretty_print=True, xml_declaration=True, encoding="UTF-8").decode()
    sys.stdout.write(xml)

if __name__ == "__main__":
    getGamaXml()