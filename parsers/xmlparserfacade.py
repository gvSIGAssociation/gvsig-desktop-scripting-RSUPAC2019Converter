# encoding: utf-8

import gvsig

from gvsig import geom 

from org.gvsig.fmap.crs import CRSFactory
from org.gvsig.tools import ToolsLocator

from addons.RSUPAC2019Importer.parsers.rsuparser import RSUParser
from addons.RSUPAC2019Importer.trace import trace, trace_remove

def create_parser(status):
  return XMLReaderFacade(status)

class XMLReaderFacade(object):
  def __init__(self, status):
    self.status = status
    self.dbwriter = None
    self.count = 0

  def close(self):
    # Se la llama cuando se termina de usar el lector de xml
    # para que cierre/libere los recursos que pueda estar usando
    pass

  def getCount(self, xmlfile):
    # Recive un File a un XML y devuelve cuantas entidades SRU hay
    # en el fichero XML.
    # Patatera, pero esta implementacion puede servirnos.
    self.count = 0
    f = open(xmlfile.getAbsolutePath(),"r")
    for line in f.xreadlines():
      if "</rsu>" in line.lower():
        self.count += 1
    f.close()
    return self.count
  
  def parse(self, dbwriter, xmlfile): 
    # Recive un DBWriter y un File al XML y parsea el XML
    # llamando al writer para escribir los datos en la BBDD
    # Cada vez que lee un registo SRU debe llamar a self.status.incrementCurrentValue()

    # Esta implementacion es para poder probar el dbwriter.
    self.dbwriter = dbwriter
    e = dict()
    e["CA_Expediente"] = "17"
    e["ProvExpediente"] = "46"
    e["CRExpediente"] = "000"
    e["NumExpediente"] = "104622002446"
    e["Fregistro"] = "2019-04-23"
    e["Fmodificacion"] = "2019-05-24"
    e["TitComp_Solicitante"] = "N"
    e["Extran_Conyuge_Solicitud"] = "S"

    p = dict()
    p["SupRecintoDec"] = "17"
    p["ProvMuni"] = "46"
    p["ID_PARCELA"] = "123"
    g = geom.createGeometry(geom.POLYGON, geom.D2) 
    g.addVertex(geom.createPoint(geom.D2,0,0))
    g.addVertex(geom.createPoint(geom.D2,10,10))
    g.addVertex(geom.createPoint(geom.D2,10,0))
    g.addVertex(geom.createPoint(geom.D2,0,0))
    g.setProjection(CRSFactory.getCRS("EPSG:4326"))
    idrecinto = 1
    for ne in xrange(self.count):
      for np in xrange(6):
        p["ID_RECINTO"] = idrecinto
        idrecinto += 1
        if np % 2 == 0:
          p["GEOMETRY"] = None
        else:
          p["GEOMETRY"] = g
        self.dbwriter.insert("RSUPAC2019_RECINTOS_SIGPAC", **p)
      e["CRExpediente"] = "%03d" % ne
      e["NumExpediente"] = "10462200244%d" % ne
      self.dbwriter.insert("RSUPAC2019_EXPEDIENTES", **e)
      self.status.incrementCurrentValue()


def test():
  import os
  from java.io import File

  #from addons.RSUPAC2019Importer.parsers.xmlparser0 import create_parser
  #from addons.RSUPAC2019Importer.parsers.xmlparserfacade import create_parser

  #from addons.RSUPAC2019Importer.writers.shpwriter import create_writer
  from addons.RSUPAC2019Importer.writers.writerfacade import create_writer

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
