# encoding: utf-8

import gvsig

from org.gvsig.tools import ToolsLocator

from addons.RSUPAC2019Converter.writers.rsuwriter import RSUWriter
from addons.RSUPAC2019Converter.trace import trace, trace_format, trace_remove

def create_writer(status=None):
  return WriterFacade(status)

class WriterFacade(RSUWriter):

  def __init__(self, status=None):
    RSUWriter.__init__(self, status)

  def create(self):
    trace("CREATE")
    
  def drop(self):
    trace("DROP")
    
  def edit(self):
    trace("EDIT BEGIN")
    
  def finishEditing(self):
    trace("EDIT END")
      
  def cancelEditing(self):
    trace("EDIT CANCEL")

  def insert(self, tableName, **values):
    trace("INSERT INTO %s VALUES %s" % (tableName,trace_format(values)))


def test():
  import os
  from java.io import File

  #from addons.RSUPAC2019Converter.parsers.xmlparser0 import create_parser
  from addons.RSUPAC2019Converter.parsers.xmlparserfacade import create_parser

  #from addons.RSUPAC2019Converter.writers.shpwriter import create_writer
  #from addons.RSUPAC2019Converter.writers.writerfacade import create_writer

  trace_remove()
  try:
    os.remove("/tmp/srupac2019.shp")
  except:
    pass
    
  taskManager = ToolsLocator.getTaskStatusManager()

  status = taskManager.createDefaultSimpleTaskStatus("SRU PAC")

  source = File(gvsig.getResource(__file__,"..","datos","test","RSU_PAC_2019_extra.xml"))
  source = File("/home/jjdelcerro/BDA_RSU_PAC19_1723072019_001.XML")
  target = File("/tmp/srupac2019.shp")
  
  parser = create_parser(status, source)
  writer = create_writer(status, target)

  writer.drop()
  writer.create()
  
  writer.edit()
  parser.parse(writer)
  writer.finishEditing()


def main(*args):
  pass
  