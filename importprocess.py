# encoding: utf-8

import gvsig

import traceback

from java.lang import Runnable
from java.lang import Thread
import java.lang.Exception 

from org.gvsig.fmap.dal import DALLocator

class ImportProcess(Runnable):
  def __init__(self, parsers, writer, status, create=True):
    self.parsers = parsers
    self.writer = writer
    self.status = status
    self.create = create
    
  def run(self):
    try:
      if self.create :
        self.status.message("Preparando destino...")
        self.writer.drop()
        self.writer.create()

      count = 0
      for parser in self.parsers:
        count += parser.getCount()
      
      self.status.setRangeOfValues(0,count)
      self.status.setCurValue(0)

      self.status.message("Cargando...")

      self.writer.edit()
      for parser in self.parsers:
        parser.parse(self.writer)
      self.writer.finishEditing()
      
      self.status.message("Importacion completada")
      self.status.terminate()

    except java.lang.Exception, ex:
      print "[J] Error importing data"
      ex.printStackTrace()
      traceback.print_exc()
      self.status.setTitle("ERROR. " + self.status.getTitle())
      self.status.abort()
      if self.writer!=None:
        self.writer.finishEditing()
        #self.writer.cancelEditing()
    
    except:
      print "[P] Error importing data"
      traceback.print_exc()
      self.status.setTitle("ERROR. " + self.status.getTitle())
      self.status.abort()
      if self.writer!=None:
        self.writer.finishEditing()
        #self.writer.cancelEditing()

    finally:
      for parser in self.parsers:
        if parser!=None:
          try:
            parser.close()
          except:
            pass
      
def createImportProcess(source, target, status, **kwargs):
  return ImportProcess(source, target, status, **kwargs)

def main(*args):
    pass
