#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

"""
Autotest console client
Manages autotested projects

Usage: cautotest [opts] [args]

-h, --help                              show this message
-a project_name code_dir tests_dir      add project
-e project_name code_dir tests_dir      edit project
-d project_name                         delete project
-l                                      list projects
-i project_name                         get project info
"""

__author__ = 'Danilenko Alexander'
__email__ = 'hdg700@gmail.com'


import sys
import getopt
import os
from cautotest import *


class UsageError(Exception):
    """Exception raised for printing help message"""
    def __init__(self, msg='', help_only=False):
        self.msg = msg
        self.help_only = help_only

class InvalidArgs(Exception):
    """Exception raised when arguments are invalid"""
    def __init__(self, msg=''):
        self.msg = msg


class ArgumentsValidator(object):
    """Validates command line arguments"""
    def __init__(self):
        pass

    def validate(self, action, args):
        """Validates arguments for specified action"""
        try:
            self.__getattribute__(action)(args)
        except AttributeError:
            raise InvalidArgs(u'unrecognized action')

    def add(self, args):
        """Validates add project action"""
        if len(args) != 3:
            raise InvalidArgs(u'invalid arguments count')

        if not os.path.isdir(args[1]):
            raise InvalidArgs(u'\'{0}\' is not a valid code directory'.format(args[1]))

        if not os.path.isdir(args[2]):
            raise InvalidArgs(u'\'{0}\' is not a valid tests directory'.format(args[2]))

    def edit(self, args):
        """Validates edit project action"""
        if len(args) != 3:
            raise InvalidArgs(u'invalid arguments count')

        if not os.path.isdir(args[1]):
            raise InvalidArgs(u'\'{0}\' is not a valid code directory'.format(args[1]))

        if not os.path.isdir(args[2]):
            raise InvalidArgs(u'\'{0}\' is not a valid tests directory'.format(args[2]))

    def delete(self, args):
        """Validates delete project action"""
        if len(args) != 1:
            raise InvalidArgs(u'invalid arguments count')

    def info(self, args):
        """Validates info project action"""
        if len(args) != 1:
            raise InvalidArgs(u'invalid arguments count')

    def list(self, args):
        """Validates projects list action"""
        if len(args) != 0:
            raise InvalidArgs(u'invalid arguments count')


def main(argv=None):
    """Parse command line arguments"""
    if not argv:
        argv = sys.argv[1:]

    try:
        action = 'add'
        try:
            opts, args = getopt.getopt(argv, 'ahedil',
                    ['help', 'edit', 'delete', 'info', 'list'])

            for o, a in opts:
                if o in ['-h', '--help']:
                    raise UsageError(help_only=True)
                elif o in ['-a']:
                    action = 'add'
                    break
                elif o in ['-e, --edit']:
                    action = 'edit'
                    break
                elif o in ['-d', '--delete']:
                    action = 'delete'
                    break
                elif o in ['-i', '--info']:
                    action = 'info'
                    break
                elif o in ['-l', '--list']:
                    action = 'list'
                    break

        except getopt.error as e:
            raise UsageError(e)

        v = ArgumentsValidator()
        v.validate(action, args)

        try:
            atc = AutotestConsole()
            atc.do_action(action, args)
        except ClientException as e:
            print e.msg
            print

    except UsageError as e:
        if e.help_only:
            print __doc__
        else:
            print e.msg
            print u'Use --help for more information'
            print

    except InvalidArgs as e:
        print u'Arguments error:', e.msg
        print u'Use --help for more information'
        print


if __name__ == '__main__':
    sys.exit(main())
