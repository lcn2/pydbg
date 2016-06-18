'''\
dbg - General debugging facilities

Using syslog-like levels and debug verbosity control,
make it easy for python code to imbed fine grain
debugging control as well as issuing notices, warnings,
fatal errors / system errors.

Usage example:

from dbg import Dbg

d = Dbg(stderr=True, verbosity_floor=3)

d.dbg(4, 'This level 4 message will print bacause verbosity_floor =', d.verbosity_floor)

'''

# Stuff we need
import sys
import os
import logging
from logging import handlers


class Dbg(object):
    '''\
    General debugging facility class

    usage example:
    d = Dbg(stderr=True, verbosity_floor=3)
    '''

    def __init__(self, name, stdout=False, stderr=True, syslog=False, tofile='', verbosity_floor=0):
        'Debug initializer'

        LINUX_LOG_DEV = '/dev/log'

        fmt = logging.Formatter('%(levelname)s %(name)s %(asctime)s %(message)s')
        lvl = logging.DEBUG

        # emit only debug messages below the verbosity floor level
        self.verbosity_floor = verbosity_floor

        # our named logging facility
        self.log_op = logging.getLogger(name)
        self.log_op.setLevel(lvl)
        self.log_op.propagate = False

        # stream handler for stderr if enabled
        if stderr:
            errhdlr = logging.StreamHandler(sys.stderr)
            errhdlr.setLevel(lvl)
            errhdlr.setFormatter(fmt)
            self.log_op.addHandler(errhdlr)

        # stream handler for stdout if enabled
        if stdout:
            outhdlr = logging.StreamHandler(sys.stdout)
            outhdlr.setLevel(lvl)
            outhdlr.setFormatter(fmt)
            self.log_op.addHandler(outhdlr)

        self.handlers = self.log_op.handlers[:]

        # stream handler for syslog if enabled
        if syslog:
            if os.path.exists(LINUX_LOG_DEV):
                syslog_dev = LINUX_LOG_DEV
            else:
                syslog_dev = ''

            if syslog_dev:
                syshdlr = handlers.SysLogHandler(address=syslog_dev, facility=handlers.SysLogHandler.LOG_DAEMON)
            else:
                syshdlr = handlers.SysLogHandler(facility=handlers.SysLogHandler.LOG_DAEMON)
            syshdlr.setLevel(lvl)
            syshdlr.setFormatter(fmt)
            self.log_op.addHandler(syshdlr)

        # file handler if enabled
        if tofile:
            fhdlr = logging.FileHandler(tofile)
            fhdlr.setLevel(lvl)
            fhdlr.setFormatter(fmt)
            self.log_op.addHandler(fhdlr)

    def __log(self, caller_name, severity, level, message, *args):
        'Log a debugging message if our verbosity floor is high enough'

        # print a debug message only if permitted by the verbosity floor level
        if level <= self.verbosity_floor:
            self.log_op.log(severity, 'from: {cn} {mg} {ag}'.format(cn=caller_name, mg=message, ag=' '.join(args)))

    def dbg(self, level, message, *args):
        'Log a debugging message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        self.__log(caller_name, 10, level, message, *args)

    def info(self, level, message, *args):
        'Log an info message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        self.__log(caller_name, 20, level, message, *args)

    def warning(self, level, message, *args):
        'Log a warning message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        self.__log(caller_name, 30, level, message, *args)

    def error(self, level, message, *args):
        'Log an error message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        self.__log(caller_name, 40, level, message, *args)

    def critical(self, level, message, *args):
        'Log a critical message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        self.__log(caller_name, 50, level, message, *args)

    def close_handers(self):
        for handler in self.handlers:
            handler.close()
            self.log_op.removeHandler(handler)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_handers()

if __name__ == '__main__':
    # setup debugging facility

    with Dbg(stderr=True, syslog=True, tofile='/tmp/log.log', verbosity_floor=3) as d:
        # emit a debug message above the floor
        d.dbg(2, 'This level 2 message should appear because the',
                  'verbosity floor = ' + str(d.verbosity_floor))

        # this debug message should not appear
        d.error(4, 'This level 4 message should NOT appear because the',
                  'verbosity floor = ' + str(d.verbosity_floor))


