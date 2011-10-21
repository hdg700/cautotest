# -*- coding: utf-8 -*-

"""
Autotest console client module
"""

__author__ = 'Danilenko Alexander'
__email__ = 'hdg700@gmail.com'


import os
import dbus


class AutotestConsole(object):
    """Autotest console client class"""
    def __init__(self):
        """Inits dbus-session"""
        pass

    def do_action(self, action, args):
        """Does specified action"""
        try:
            self.__getattribute__(action)(args)
        except AttributeError:
            pass
