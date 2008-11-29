"""\
RunningStat lets you compute running variance and means.  It's nice if you
don't have access to all the data at once, and takes little memory besides.

>>> rs = running_stat.RunningStat()
>>> for x in xrange(1e6): rs.add(x)
>>> rs.mean(), rs.var(), rs.std()
(499999.5, 83333333333.249985, 288675.13459466852)

 
var() and std() are alternatives to NumPy's var() and std() (though only for 1d
data).  They are good for very large arrays because they do not create any
intermediate data structures, and do a minimal amount of data type conversion
(= copying!).  Furthermore, at least on my machine they are faster than NumPy:

In [1]: from numpy import *
In [2]: x = arange(1e8)                      # python process RSIZE = 774 MB

In [3]: timeit -n1 -r5 std(x)                # RSIZE goes as high as 2.2 GB
1 loops, best of 5: 4.01 s per loop          # (3x size = two temp arrays?)

In [4]: import running_stat

In [5]: timeit -n1 -r5 running_stat.std(x)   # RSIZE = 774 MB the whole time
1 loops, best of 5: 1.66 s per loop


questions to brendan o'connor, brenocon@gmail.com, anyall.org
"""
# use swig for the class
from rs_ext import RunningStat


# use ctypes for the functions

import sys, os.path
this_dir = os.path.dirname(sys.modules[__name__].__file__)

from ctypes import cdll, c_void_p, c_uint, c_double
EXT = cdll.LoadLibrary(os.path.join(this_dir, '_rs_ext.so'))

try:
  import numpy as np
  typemap = {
    np.dtype('double'):  EXT.running_var_double,
    np.dtype('float32'): EXT.running_var_float,
    np.dtype('int8'):    EXT.running_var_char,
    np.dtype('uint8'):   EXT.running_var_uchar,
    np.dtype('int16'):   EXT.running_var_short,
    np.dtype('uint16'):  EXT.running_var_ushort,
    np.dtype('int32'):   EXT.running_var_long,
    np.dtype('uint32'):  EXT.running_var_ulong,
  }
  # they dont appear in EXT.__dict__ until you reference them like above
  running_functions = [f for name,f in EXT.__dict__.items() if name.startswith('running_')]
  for f in running_functions:
    f.argtypes = [c_void_p,c_uint]
    f.restype = c_double
except ImportError: pass


def var(x):
  " x is a numpy array "
  if x.dtype in typemap:
    return typemap[x.dtype](x.ctypes.data, len(x))
  x = np.double(x)
  return EXT.running_var_double(x.ctypes.data, len(x))

def std(x):
  " x is a numpy array "
  return np.sqrt(var(x))
  #import math
  #return math.sqrt(var(x))
  


# hm.  np.var() looks wrong on float32, we look better
# % python __init__.py
# float64   np.var 8.33333333333e+12     np.std 2886751.34595       
#           rs.var 8.33333333333e+12     rs.std 2886751.34595       
# float32   np.var 8.30085011522e+12     np.std 2881119.59405       
#           rs.var 8.33333333333e+12     rs.std 2886751.34595       

if __name__=='__main__':
  for d in [np.double,np.float32,np.int8,np.uint8,np.int16,np.uint16,np.int32,np.uint32]:
    x = np.arange(1e7, dtype=d)
    print "%-9s np.var %-20s  np.std %-20s" % (x.dtype.name, np.var(x), np.std(x))
    print "%-9s rs.var %-20s  rs.std %-20s" % ('', var(x), std(x))

