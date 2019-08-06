# encoding: utf-8

import gvsig

import traceback

from java.lang import Runnable
from java.lang import Thread
import java.lang.Exception 

from org.gvsig.fmap.dal import DALLocator

class ImportProcess(Runnable):
  def __init__(self, parser, writer, status, xmlfiles, create=True):
    self.parser = parser
    self.writer = writer
    self.status = status
    self.create = create
    self.xmlfiles = xmlfiles
    
  def run(self):
    try:
      if self.create :
        self.status.message("Preparando destino...")
        self.writer.drop()
        self.writer.create()

      self.status.message("Estimando numero de expedientes...")
      count = 0
      for xmlfile in self.xmlfiles:
        count += self.parser.getCount(xmlfile)
      
      self.status.setRangeOfValues(0,count)
      self.status.setCurValue(0)

      self.status.message("Cargando...")

      self.writer.edit()
      self.status.message("Convirtiendo expedientes")
      for xmlfile in self.xmlfiles:
        self.parser.parse(xmlfile, self.writer)
      self.status.message("Cerrando ficheros")
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
      
def createImportProcess(source, target, status, xmlfiles, **kwargs):
  return ImportProcess(source, target, status, xmlfiles, **kwargs)

def main(*args):
    pass
