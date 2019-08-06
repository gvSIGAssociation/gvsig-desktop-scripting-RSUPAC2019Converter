# encoding: utf-8

import gvsig

class RSUParser(object):
  """Clase base/interface de la que deben extender todos los parsers"""
  def __init__(self, status, xmlfile):
    self.status = status
    self.xmlfile = xmlfile

  def close(self):
    pass
    
  def getCount(self):
    return 0

  def parse(self, writer): 
    pass
    
def main(*args):
  pass
