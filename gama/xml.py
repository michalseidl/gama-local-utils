# -*- coding: utf-8 -*-

"""
Module with helper function for GNU Gama XML manipulation
"""

import lxml.etree as et
from collections import OrderedDict

from . import utils


def initGamaXml(config):
    """
    Returns etree element with initialized Gama XML
    :param config:
    :return: Gama XML etree element
    """

    DOCTYPE = '<?xml version="1.0">'

    # xml header
    gamaLocal = et.Element('gama-local', xmlns=config['XMLNS'])
    et.SubElement(gamaLocal, 'network', attrib=config['network'])
    et.SubElement(gamaLocal.find('network'), 'description')
    gamaLocal.find('network/description').text = config['description']
    et.SubElement(gamaLocal.find('network'), 'parameters', attrib=config['parameters'])

    return gamaLocal

def addPointEl(pointsObservations, data):
    """
    Adds point to points-observations element
    :param pointsObservations:
    :param data:
    :return: pointEl
    """

    # If point is str just add id
    if isinstance(data, str):
        pointEl = et.SubElement(pointsObservations, 'point',
            attrib=OrderedDict([('id', data.upper()), ('adj', 'xyz')]))

    # if point has all 3 coordinates
    elif len(data) > 3:
        pointEl = et.SubElement(pointsObservations, 'point',
            attrib=OrderedDict([('id', data[0].upper()),
                ("x", data[1]), ("y", data[2]), ("z", data[3]), ("adj", 'XYZ')]))

    return pointEl

def updatePointEl(pointEl, point, pointSettings):
    """
    Updates point element with point data
    :param pointEl:
    :param point:
    :param pointSettings:
    :return: pointEl
    """

    if pointEl.get('id') == point[0]:

        # Clear all attributes and set new one
        # BUG lxml clear influence intendation
        # pointEl.clear()
        # pointEl.set('id',point[0])
        if 'fix' in pointEl.attrib:
            pointEl.attrib.pop('fix')
        if 'adj' in pointEl.attrib:
            pointEl.attrib.pop('adj')

        pointEl.set('x', point[1])
        pointEl.set('y', point[2])
        pointEl.set('z', point[3])

        # Set settings from pointSettings
        if pointEl.get('id') in pointSettings:
            if 'fix' in pointSettings[pointEl.get('id')]:
                pointEl.set('fix', pointSettings[pointEl.get('id')]['fix'])
            if 'adj' in pointSettings[pointEl.get('id')]:
                pointEl.set('adj', pointSettings[pointEl.get('id')]['adj'])

        # Set default settings
        else:
            pointEl.set('adj', 'XYZ')

    return pointEl

def addObsEl(pointsObservations, data):
    """
    Adds obs to points-observations element
    :param pointsObservations:
    :param data:
    :return: obsEl
    """

    obsEl = et.SubElement(pointsObservations, 'obs',
        attrib=OrderedDict([('from', data[0]),('from_dh', data[1])]))

    return obsEl

def addDirEl(obs, data):
    """
    Adds dir to obs element
    :param pointsObservations:
    :param data:
    :return: dirEl
    """

    dirEl = et.SubElement(obs, 'direction',
        attrib=OrderedDict([('to', data[0]), ('val', data[3]), ('stdev', utils.getStdDev('direction', data))]))

    return dirEl

def addDistEl(obs, data):
    """
    Adds horiz. distance to obs element, expects slope distance in data
    :param pointsObservations:
    :param data:
    :return: distEl
    """

    distEl = et.SubElement(obs, 'distance',
        attrib=OrderedDict([('to', data[0]),
            ("val", str(utils.redSdist(data))),("stdev", utils.getStdDev('distance', data))]))

    return distEl

def addSdistEl(obs, data):
    """
    Adds slope distance to obs element
    :param pointsObservations:
    :param data:
    :return: sDistEl
    """

    sDistEl = et.SubElement(obs, 's-distance',
        attrib=OrderedDict([('to', data[0]), ('to_dh', data[2]),
            ("val", data[1]), ("stdev", utils.getStdDev('s-distance', data))]))

    return sDistEl

def addZangleEl(obs, data):
    """
    Adds zenit angle to obs element
    :param pointsObservations:
    :param data:
    :return: zAngletEl
    """

    zAngleEl = et.SubElement(obs, 'z-angle',
        attrib=OrderedDict([('to', data[0]), ('to_dh', data[2]),
            ("val", data[1]), ("stdev", utils.getStdDev('z-angle', data))]))

    return zAngleEl