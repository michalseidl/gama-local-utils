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
from settings import XML_SETTINGS, COOR_SETTINGS, pointSettings

def __parseCoorStdin():
    """
    Reads coors from STDIN
    :return: dataList
    """

    dataList = list()

    for line in sys.stdin:

        # Split line into coordinate data
        if line.find(',') != -1:
            lineData = line.strip().split(',')
        else:

            lineData = line.strip().split()

        lineData[0] = lineData[0].upper()
        dataList.append(lineData)

    dataList.sort(key=lambda x: x[0])

    return dataList

def testCoorFile(COOR_SETTINGS):
    """
    Test format and duplicit number in coordinate file
    :param COOR_SETTINGS:
    :return: TXT to STDOUT and STDERR
    """

    pointList = __parseCoorStdin()
    #sys.stderr.write('{:8s} {:8s} {:14s} {:14s} {:14s}\n'.format(*('p1','p2', 'dx','dy','dz')))

    for point in pointList:
        pointName = point[0].split('.')
        # Only if not control point (no dot in string)
        if len(pointName) == 1:
            diffList = []
            controlPointList = [point]
            # Loop to find control point
            for control in pointList:
                if point[0] != control[0]:
                    controlName = control[0].split('.')
                    if len(controlName) == 2:
                        # Compute diff in control point found
                        if pointName[0] == controlName[0]:
                            controlPointList.append(control)
                            diff = [float(a)-float(b) for a,b in zip(point[1:4], control[1:4])]
                            diffList.append([point[0], control[0]]+diff)

                    elif len(controlName) > 2:
                        sys.stderr.write(''.join(('Wrong control point name: ', control[0],'\n')))

                # Compute diff against itself, can be computed mean values laters
                elif point[0] == control[0]:
                    diff = [float(a) - float(b) for a, b in zip(point[1:4], control[1:4])]
                    diffList.append([point[0], control[0]] + diff)

            if len(diffList) > 1:

                sys.stderr.write('Point : {}\n'.format(point[0]))
                sys.stderr.write('==================\n')

                for control in controlPointList:
                    sys.stderr.write('{:8s} {:13.3f} {:13.3f} {:10.3f}\n'
                        .format(*control[0:1] + [float(x) for x in control[1:4]]))

                meanX = sum([x[2] for x in diffList]) / float(len(diffList))
                meanY = sum([x[3] for x in diffList]) / float(len(diffList))
                meanZ = sum([x[4] for x in diffList]) / float(len(diffList))

                sys.stderr.write('Point coordinates differences:\n')
                for diff in diffList:
                    # Print diff values
                    sys.stderr.write('{:8s} {:10.3f} {:10.3f} {:10.3f}\n'
                        .format(*(diff[1:2]+[m-x for m,x in zip([meanX,meanY,meanZ],diff[2:])])))

                # TODO Test differences against max values

                # Print average values, first point coor (zero diffs) - mean
                sys.stderr.write('Point average coordinates:\n')
                pStr = '{:8s} {:13.3f} {:13.3f} {:10.3f}\n'\
                    .format(*[diff[0],] + [float(x)-m for m,x in zip([meanX, meanY, meanZ], point[1:4])])

                sys.stderr.write(pStr)
                sys.stdout.write(pStr)

            else:
                sys.stdout.write('{:8s} {:13.3f} {:13.3f} {:10.3f}\n'
                    .format(*[point[0], ] + [float(x) for x in point[1:4]]))

        # TODO check single point with '.' in list







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
        if sys.argv[1] != 'test':
            gamaXmlFilePath = sys.argv[1]
            coor2gamaXml(gamaXmlFilePath, pointSettings)
        else:
            testCoorFile(COOR_SETTINGS)
    else:
        getGamaXml(XML_SETTINGS)