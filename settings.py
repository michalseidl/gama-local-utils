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
    '611': {'fix': 'xy', 'adj': 'Z'}
}

COOR_SETTINGS = {
    'xMax': 0.05,
    'yMax': 0.05,
    'zMax': 0.05
}

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