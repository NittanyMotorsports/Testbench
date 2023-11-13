"""
This is a file with utility functions
"""

import os

def aliased_port(alias):
    """
    Function that returns port give an aliased name from a udev rule

    args:
        - alias:
            string of aliased port i.e. "device"
    returns:
        - port:
            string of actual port i.e. "ttyUSB0"
    """
    for filename in os.listdir('/dev'):
        if filename.startswith(alias):
            return os.readlink(os.path.join('/dev', filename))
            # return port.split('/')[-1].lstrip('ttyUSB')
