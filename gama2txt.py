#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Converts Gama XML output file into TXT report
Restriction:
- no mx my mz are computed for point
"""

import sys
import lxml.etree as et

def parserPointEl(pointEl):
    """
    Parser element into list
    :param pointEl: etree.Element
    :return: point: list
    """
    point = [None, float('NaN'), float('NaN'), float('NaN')]

    for item in pointEl:
        # Can not be used simple el.tag because involves namespace
        tag = item.xpath('local-name()')
        if tag == 'id':
            point[0] = item.text
        elif tag == 'x' or tag == 'X':
            point[1] = float(item.text)
        elif tag == 'y' or tag == 'Y':
            point[2] = float(item.text)
        elif tag == 'z' or tag == 'Z':
            point[3] = float(item.text)

    return point

def parserObsEl(obsEl):
    """
    Parser obs into list
    :param obsEl: etree.Element
    :return: obs: list
    """
    obs = [None, None, float('NaN'), float('NaN')]

    for item in obsEl:
        # Can not be used simple el.tag because involves namespace
        tag = item.xpath('local-name()')
        if tag == 'from':
            obs[0] = item.text
        elif tag == 'to':
            obs[1] = item.text
        elif tag == 'obs':
            obs[2] = float(item.text)
        elif tag == 'adj':
            obs[3] = float(item.text)

    return obs

def gamaXml2coor(gamaXmlFilePath):
    """
    Parse XML and writes coordinates and observation to STDOUT
    :param gamaXmlFilePath:
    :return: TXT to STDOUT
    """

    gamaLocal = et.parse(gamaXmlFilePath)

    NSMAP = {'gl': gamaLocal.xpath('namespace-uri(.)')}
    dirMax = 0.0100
    distMax = 0.02
    zAngMax = 0.0100

    # Coordinates

    corFixedXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:coordinates/gl:fixed/gl:point',
        namespaces = NSMAP)

    corAproxXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:coordinates/gl:approximate/gl:point',
        namespaces=NSMAP)

    corAdjXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:coordinates/gl:adjusted/gl:point',
        namespaces=NSMAP)

    #gamaLocalRoot = gamaLocal.getroot()
    #print(gamaLocalRoot.tag)
    #coordinates = gamaLocalRoot.findall('gl:coordinates', namespaces = NSMAP)

    corFixed = list()
    for element in corFixedXml:
        corFixed.append(parserPointEl(element))

    corAprox = list()
    for element in corAproxXml:
        corAprox.append(parserPointEl(element))

    corAdj = list()
    for element in corAdjXml:
        corAdj.append(parserPointEl(element))


    #pointList = list()
    #pointList.append(['fixed', corFixed, len(corFixed)])
    #pointList.append(['aprox', corAprox, len(corAprox)])
    #pointList.append(['adj', corAdj, len(corAdj)])

    for pointFixed in corFixed:
        sys.stdout.write("{:5s} {:12.3f} {:12.3f} {:10.3f}"
                         "\n".format(*pointFixed))

    sys.stdout.write("\n")

    for pointAprox in corAprox:
        for pointAdj in corAdj:
            if pointAdj[0] == pointAprox[0]:
                sys.stdout.write("{:5s} {:12.3f} {:12.3f} {:10.3f}"
                                 " {:12.3f} {:12.3f} {:12.3f}"
                                 " {:10.3f} {:10.3f} {:10.3f}"
                                 "\n".format(*(pointAdj+pointAprox[1:]+[a-b for a,b in zip(pointAdj[1:],pointAprox[1:])])))

    sys.stdout.write("\n")

    # Measurements
    obsDirXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:observations/gl:direction',
        namespaces = NSMAP)

    obsSlopeDistXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:observations/gl:slope-distance',
        namespaces = NSMAP)

    obsZenitAnglXml = gamaLocal.xpath('/gl:gama-local-adjustment/gl:observations/gl:zenith-angle',
        namespaces=NSMAP)


    obsDir = list()
    for element in obsDirXml:
        obsDir.append(parserObsEl(element))

    obsSlopeDist = list()
    for element in obsSlopeDistXml:
        obsSlopeDist.append(parserObsEl(element))

    obsZenitAngl = list()
    for element in obsZenitAnglXml:
        obsZenitAngl.append(parserObsEl(element))

    for obs in obsDir:
        if abs(obs[3] - obs[2]) > dirMax:
            sys.stdout.write("{:5s} {:5s} {:10.4f} {:10.4f} {:10.4f}"
                         "\n".format(*obs+[obs[3] - obs[2]]))

    sys.stdout.write("\n")

    for obs in obsSlopeDist:
        if abs(obs[3] - obs[2]) > distMax:
            sys.stdout.write("{:5s} {:5s} {:10.4f} {:10.4f} {:10.4f}"
                             "\n".format(*obs + [obs[3] - obs[2]]))

    sys.stdout.write("\n")

    for obs in obsZenitAngl:
        if abs(obs[3] - obs[2]) > zAngMax:
            sys.stdout.write("{:5s} {:5s} {:10.4f} {:10.4f} {:10.4f}"
                             "\n".format(*obs + [obs[3] - obs[2]]))

if __name__ == "__main__":

    if len(sys.argv) == 2:
        gamaXmlFilePath = sys.argv[1]
        gamaXml2coor(gamaXmlFilePath)