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

        except dbus.exceptions.DBusException as e:
            print e
            raise ClientException('DBus error: autotest daemon doesn\'t provide sush method')

    def add(self, project, code_dir, test_dir):
        code_dir = os.path.realpath(code_dir)
        test_dir = os.path.realpath(test_dir)

        res = self.daemon.dbus_add(project, code_dir, test_dir,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')
        print res

    def edit(self, project, name, code_dir, test_dir):
        res = self.daemon.dbus_edit(project, name, code_dir, test_dir,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')
        print res

    def delete(self, project):
        res = self.daemon.dbus_delete(project,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')
        if not res:
            print 'Error deleting project'
        else:
            print res

    def info(self, project):
        res = self.daemon.dbus_info(project,
                dbus_interface='hdg700.autotestd.AutotestDaemon.client')

        if not res:
            print 'No such project!'
            return False

        print 'Project:'.rjust(10), res['name']
        print 'Code dir:'.rjust(10), res['code_dir']
        print 'Test dir:'.rjust(10), res['test_dir']
        print 'Classes:'.rjust(10), res['code_count']
        print 'Tests:'.rjust(10), res['test_count']
        print

    def list(self):
        res = self.daemon.dbus_list(dbus_interface='hdg700.autotestd.AutotestDaemon.client')
        if res:
            print 'Active projects:'
            for i in res:
                print '\t- ' + i[0]
            print
            print 'Use \'-i project_name\' for more information'
            print
        else:
            print 'No active projects'
            print
