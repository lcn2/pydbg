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
import logging


class Dbg:
    '''\
    General debugging facility class

    usage example:
    d = Dbg(stderr=True, verbosity_floor=3)
    '''

    def __init__(self, stderr=True, verbosity_floor=0):
        'Debug initializer'
        
        # How we standardize log message strings
        logging.basicConfig(
            level = logging.DEBUG,
            # format = '%(levelname)-8s %(name)-13s %(asctime)s %(message)s',
            format = '%(levelname)s %(name)s %(asctime)s %(message)s',
            # filename = 'tmp.log'
        )

        # emit only debug messages below the verbosity floor level
        self.verbosity_floor = verbosity_floor

        # our named logging facility for stderr
        self.LOG = logging.getLogger(__name__)

        # enable or disable debugging to stderr
        self._write_to_stderr = stderr

    def dbg(self, level, message, *args):
        'Log a debugging message if our verbosity floor is high enough'

        # obtain the name of our caller as a string
        caller_name = sys._getframe().f_back.f_code.co_name

        # print a debug message only if permited by the verbosity floor level
        if level <= self.verbosity_floor:
            if self._write_to_stderr:
                self.LOG.debug('from: ' + caller_name + ': ' + message + ' '.join(args))


if __name__ == '__main__':
    # setup debugging facility
    d = Dbg(stderr=True, verbosity_floor=3)

    # emit a debug message above the floor
    d.dbg(2, 'This level 2 message should appear because the ',
              'verbosity floor = ' + str(d.verbosity_floor))

    # this debug message should not appear
    d.dbg(4, 'This level 4 message should NOT appear because the ',
              'verbosity floor = ' + str(d.verbosity_floor))
