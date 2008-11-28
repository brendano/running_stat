running_stat  -  C++ implementation of calculating running variance/standard
deviation, plus Python wrappers.

If you only want the C++, just copy out running_stat.cc (or just the class).

To build the Python library, do "python build.py".  Requires SWIG.  (I'm using
1.3.31).

build.py needs to be patched for platforms other than mac; or better, convert
to setuptools.

Brendan O'Connor - anyall.org
