running_stat - C++ implementation of calculating running variance/standard
deviation, plus Python (NumPy) wrappers.

More explanation at
http://anyall.org/blog/2008/11/calculating-running-variance-in-python-and-c/

See docstring in __init__.py for why it's great for Python.

If you only want the C++, just copy out running_stat.cc (or just the class).

To build the Python library, do "python build.py".  Requires SWIG.  (I'm using
1.3.31).

build.py needs to be patched for platforms other than mac; or better, convert
to setuptools.

by Brendan O'Connor - anyall.org

http://github.com/brendano/running_stat
