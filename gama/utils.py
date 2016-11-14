# -*- coding: utf-8 -*-

"""
Module with helper functions for geodetic data
"""

import math

ro = 200 / math.pi

def getStdDev(type, data):
    """
    Computes meas. stand. deviation based on unit value, type and data
    :param type:
    :param data:
    :return: stdDev
    """

    # Unit standard deviation
    stdDevDir = 60.
    stdDevDist = (15., 2.)
    stdDevZ = 60.


    if type == 'direction':
        stdDev = str(round(stdDevDir / (float(data[1])/100.)))
    elif type == 's-distance' or type == 'distance':
        stdDev = str(round(stdDevDist[0] + stdDevDist[1]*float(data[1])/1000))
    elif type == 'z-angle':
        stdDev = str(round(stdDevZ / (float(data[1]) / 100.)))

    return stdDev

def redSdist(data):
    """
    Reduce slope distance to horizontal
    :param data:
    :return: dist
    """
    dist = float(data[1]) * math.sin(float(data[4]) / ro)

    return dist