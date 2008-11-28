# i'm too lazy to figure out how to use distutils/setuptools.  lame i know
import os,sys

def sh(cmd):
  print cmd
  r = os.system(cmd)
  if r: raise Exception("Command exited %d:  %s" %(r, cmd))
  return r

if sys.platform == 'darwin':
  linker_flag = "-bundle"
else:
  raise Exception("edit this please, -shared i think?")

sh("swig -c++ -module rs_ext -python running_stat.cc")
sh("cat running_stat.cc running_stat_wrap.cxx  >  everything.cc")
sh("g++ -O3 %s -lm -lpython2.5 -I/usr/include/python2.5  everything.cc  -o _rs_ext.so" % (linker_flag,))

# g++ -g running_stat.cc -o main && ./main

