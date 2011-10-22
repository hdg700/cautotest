# -*- coding: utf-8 -*-

"""
Autotest console client module
"""

__author__ = 'Danilenko Alexander'
__email__ = 'hdg700@gmail.com'


import os
import dbus


class ClientException(Exception):
    def __init__(self, msg):
        self.msg = msg

class AutotestConsole(object):
    """Autotest console client class"""
    def __init__(self):
        """Init dbus-session"""
        try:
            bus = dbus.SessionBus()
            self.daemon = bus.get_object('hdg700.autotestd',
                    '/hdg700/autotestd/AutotestDaemon')
        except dbus.exceptions.DBusException:
            raise ClientException('DBus error: autotest daemon is not running')

    def do_action(self, action, args):
        """Call requested action"""
        try:
            self.__getattribute__(action)(*args)

        except AttributeError:
            print action, 'not found'

        except dbus.exceptions.DBusException:
            raise ClientException('DBus error: autotest daemon doesn\'t provide sush method')

    def add(self, project, code_dir, tests_dir):
        res = self.daemon.dbus_add(project, code_dir, tests_dir,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')

    def edit(self, project, code_dir, tests_dir):
        res = self.daemon.dbus_edit(project, code_dir, tests_dir,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')

    def delete(self, project):
        res = self.daemon.dbus_delete(project,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')

    def info(self, project):
        res = self.daemon.dbus_info(project,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')

    def list(self):
        res = self.daemon.dbus_list(dbus_interface='hdg700.autotestd.AutotestDaemon.client')
