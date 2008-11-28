"""
RunningStat lets you compute running variance and means.  It's nice if you
don't have access to all the data at once, and takes little memory besides.
 
var() and std() are alternatives to NumPy's array.var() amd array.std().  They
are nice for very large arrays because they do not create any intermediate data
structures, and do a minimum amount of conversion if possible.  Furthermore, at
least on my machine they are faster than NumPy:


In [1]: from numpy import *

In [2]: x=arange(1e8)                        # python RSIZE = 774 MB

In [3]: timeit -n1 -r5 std(x)                # RSIZE goes as high as 2.2 GB
1 loops, best of 5: 4.01 s per loop

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
function_lib = cdll.LoadLibrary(os.path.join(this_dir, '_rs_ext.so'))
for f in (function_lib.running_var_double, function_lib.running_var_float):
  f.argtypes = [c_void_p,c_uint]
  f.restype = c_double

def var(x):
  " x is a numpy.array "
  import numpy
  if x.dtype == numpy.double:
    pass
  elif x.dtype == numpy.float32:
    return function_lib.running_var_float(x.ctypes.data, len(x))
  else:
    x = numpy.double(x)
  return function_lib.running_var_double(x.ctypes.data, len(x))

def std(x):
  " x is a numpy.array "
  import numpy
  return numpy.sqrt(var(x))
  
