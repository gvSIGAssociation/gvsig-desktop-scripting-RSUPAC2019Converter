# encoding: utf-8

import gvsig

class RSUParser(object):
  """Clase base/interface de la que deben extender todos los parsers"""
  def __init__(self, status):
    self.status = status
    
  def close(self):
    pass
    
  def getCount(self, xmlfile):
    return 0

  def parse(self, xmlfile, writer): 
    pass
    
def main(*args):
  pass
