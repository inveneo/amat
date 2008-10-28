# app_globals.py - globls for the running application
# (c) Inveneo 2008

import string

"""The application's Globals object"""
from pylons import config

class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    SSHD_PORT = 22
    USER_PREFIX = "_"

    # sizes of database fields
    SIZE_TYPE     = 10
    SIZE_HOST     = 50
    SIZE_CUST     = 100
    SIZE_DESC     = 300
    SIZE_PER      = 18
    SIZE_OPPERIOD = 10 * SIZE_PER
    SIZE_STATUS   = 8
    SIZE_USER     = 13
    SIZE_PASS     = 32

    # string of 64 (2 ** 6) unique symbols to choose random passwords from
    PASSCHARS = string.letters + string.digits + ".="

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable
        """
        pass
