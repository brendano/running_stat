# i'm too lazy to figure out how to use setuptools.  lame i know
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
sh("g++ -O3 -lm %s -lpython2.5 -I/usr/include/python2.5 everything.cc  -o _rs_ext.so" % (linker_flag,))

#txt = open("running_stat_wrap.cxx").read()
#txt = '#include "running_stat.cc"' + '\n' + txt
#f = open("running_stat_wrap.cxx",'w')
#f.write(txt)
#f.close()
#sh("g++ -lm %s -lpython2.5 -I/usr/include/python2.5 running_stat.cc running_stat_wrap.cxx  -o _rs_ext.so" % (linker_flag,))
