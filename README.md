# pydbg
Python debug module

dbg - General debugging facilities

Using syslog-like levels and debug verbosity control,
make it easy for python code to imbed fine grain
debugging control as well as issuing notices, warnings,
fatal errors / system errors.

Usage example:

from dbg import Dbg

d = Dbg(stderr=True, verbosity_floor=3)

d.dbg(4, 'This level 4 message will print bacause verbosity_floor =', d.verbosity_floor)
