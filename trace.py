# encoding: utf-8

import gvsig

import tempfile
import pprint
import os.path

trace_counter = 0
trace_file = None

def trace_format(d):
  s = pprint.PrettyPrinter(indent=4).pformat(d)
  return s

def trace_remove():
  global trace_file

  if trace_file == None:
    trace_file = os.path.join(tempfile.gettempdir(),"trace.txt")
  try:
    os.remove(trace_file)
  except:
    pass

def trace(s):
  pass
  
def trace0(s):
  global trace_counter, trace_file

  if trace_counter < 20:
    print s
    if trace_file == None:
      trace_file = os.path.join(tempfile.gettempdir(),"trace.txt")
      
    f=open(trace_file,"a")
    f.write(s)
    f.write("\n")
    f.close()
    trace_counter += 1
