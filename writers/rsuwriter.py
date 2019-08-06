# encoding: utf-8

import gvsig

class RSUWriter(object):
  """Clase base/interface de la que deben extender todos los writers"""
  
  def __init__(self, status):
    self.status = status

  def create(self):
    pass
    
  def drop(self):
    pass
    
  def edit(self):
    pass
    
  def finishEditing(self):
    pass
      
  def cancelEditing(self):
    pass

  def insert(self, tableName, **values):
    pass


def main(*args):
    pass
