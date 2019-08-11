# encoding: utf-8

import gvsig

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal.feature import FeatureStore
from org.gvsig.fmap.dal.serverexplorer.filesystem import FilesystemServerExplorer

from org.gvsig.fmap.geom import Geometry
from org.gvsig.tools import ToolsLocator

import traceback

from addons.RSUPAC2019Converter.writers.rsuwriter import RSUWriter
from addons.RSUPAC2019Converter.trace import trace, trace_format, trace_remove

def create_writer(status, target):
  return SHPWriter(status, target)

class MemoryTable(object):
  def __init__(self, name, pkname="ID"):
    self.name = name
    self.values = dict()
    self.pkname = pkname

  def setPKName(self, pkname):
    self.pkname = pkname
    
  def insert(self, values):
    trace("INSERT INTO %s VALUES %s" % (self.name, trace_format(values)))
    pkvalue = values[self.pkname]
    self.values[pkvalue] = values
    
  def findAll(self):
    trace("FIND ALL FROM %s" % self.name)
    trace("RETURN VALUES %s" % trace_format(self.values))
    return self.values.values()
    
  def findByPK(self, pkvalue):
    trace("FIND BY PK FROM %s WHERE %r = %r" % (self.name, self.pkname, pkvalue))
    x = self.values[pkvalue]
    trace("RETURN VALUES %s" % trace_format(x))
    return x
    
  def find(self, fieldName, fieldValue):
    trace("FIND FROM %s WHERE %r = %r" % (self.name, fieldName, fieldValue))
    x = list()
    for r in self.values.values():
      if r[fieldName] == fieldValue:
        x.append(r)
    trace("RETURN VALUES %s" % trace_format(x))
    return x
    

class SHPWriter(RSUWriter):
  def __init__(self, status, targetfile):
    RSUWriter.__init__(self, status)
    self.targetfile = targetfile
    self.store = None
    self.tables = None

  def create(self):
    trace("CREATE %r" % self.targetfile)
    dataManager = DALLocator.getDataManager()
    params = dataManager.createNewStoreParameters(FilesystemServerExplorer.NAME,"Shape")
    ft = params.getDefaultFeatureType()

    ft.add("NUMEXPEDIE", "String", 21)
    ft.add("ID_PARCELA", "Integer") #"String", 25)
    ft.add("ID_RECINTO", "Integer")
    
    ft.add("R00IDSOLIC", "String",10)
    ft.add("R00SUPERFI", "Double")
    ft.add("R00AYAD", "String",100)
    ft.add("R00AYAD_SU", "String",100)
    ft.add("R00AYPDR", "String",100)

    ft.add("R10NUMORDE", "Integer")
    ft.add("R10SUPERFI", "Double")
    ft.add("R10SISEXPL", "String",2)
    ft.add("R10PRODUCT", "String",4)
    ft.add("R10VARIEDA", "String",5)
    ft.add("R10AAREAL", "String",2)
  
    ft.add("RECLINDECL", "Integer")
    ft.add("RECSUPDECL", "Double")
    ft.add("RECPROVMUN", "String", 5)
    ft.add("RECAGREGAD", "String", 4) #
    ft.add("RECZONA", "String", 2) #
    ft.add("RECPOLIGON", "String", 4) #
    ft.add("RECPARCELA", "String", 6) #
    ft.add("RECRECINTO", "String", 6) #
    
    ft.add("RECREFCATA", "String", 21)
    ft.add("RECSIGPACS", "Double")
    ft.add("RECUSIGPAC", "String", 3) #
    ft.add("RECCTRLNUE", "Boolean") #
    ft.add("RECCAPDECL", "Integer") #
    ft.add("RECSUPNETA", "Double")
    
    ft.add("RECIDARREN", "String",10)
    ft.add("RECZLN", "Boolean") #
    ft.add("RECAPRFORR", "Boolean") #
    ft.add("RECSIE", "Boolean") #
    ft.add("RECNALMEND", "Integer")
    ft.add("RECNAVELLA", "Integer")
    ft.add("RECNALGARR", "Integer")
    ft.add("RECNCASTAN", "Integer")
    ft.add("RECANOPLAN", "Integer")
    ft.add("RECSISCULH", "String",1)
    ft.add("RECID_AGPC", "String",10)
    ft.add("RECCOMPLET", "Integer")
  
    ft.add("RECAYAD", "String",100)
    ft.add("RECAYPDR", "String",100)
    ft.add("RECAYPDR_S", "String",100)
    
    ft.add("GEOMETRY","Geometry")\
      .setGeometryType(Geometry.TYPES.MULTIPOLYGON, Geometry.SUBTYPES.GEOM2D)\
      .setSRS(u'EPSG:4326')
      
    params.setCRS("EPSG:4326")
    params.setFile(self.targetfile)
    params.setGeometryType(22)
    dataManager.newStore(FilesystemServerExplorer.NAME, params.getProviderName(), params, False)

    
  def drop(self):
    trace("DROP %r" % self.targetfile)
    try:
      self.targetfile.delete()
    except:
      pass

  def getStore(self):
    if self.store == None:
      dataManager = DALLocator.getDataManager()
      parameters = dataManager.createStoreParameters("Shape")
      parameters.setCRS("EPSG:4326")
      parameters.setFile(self.targetfile)
      self.store = dataManager.openStore(parameters.getProviderName(),parameters)
    return self.store
        
  def edit(self):
    self.createInMemoryTables()
    store = self.getStore()
    if not (store.isEditing() or store.isAppending()):
      trace("BEGIN EDIT")
      store.edit(FeatureStore.MODE_APPEND)
    
    
  def finishEditing(self):
    store = self.getStore()
    if store.isEditing() or store.isAppending():
      trace("END EDIT")
      store.finishEditing()
      
  def cancelEditing(self):
    store = self.getStore()
    if store.isEditing() or store.isAppending():
      trace("CANCEL EDIT")
      store.cancelEditing()

  def getTableNames(self):
    return (
        "RSUPAC2019_EXPEDIENTES", 
        "RSUPAC2019_EXPLOTACIONES",
        "RSUPAC2019_ORIGEN_ANIMALES",
        "RSUPAC2019_AYUDA_SOL_AD",
        "RSUPAC2019_AYUDA_SOL_PDR",
        "RSUPAC2019_R10_PARCELAS", 
        "RSUPAC2019_RECINTOS_SIGPAC",
        "RSUPAC2019_RECINTOS_SIGPAC_AD",
        "RSUPAC2019_RECINTOS_SIGPAC_PDR",
        "RSUPAC2019_RECINTOS_SIGPAC_AS",
        "RSUPAC2019_RECINTOS_SIGPAC_CH",
        )

  def createInMemoryTables(self):
    self.tables = dict()
    for tableName in self.getTableNames():
      self.tables[tableName] = MemoryTable(tableName)
    self.tables["RSUPAC2019_EXPEDIENTES"].setPKName("ID_EXPEDIENTE")
    self.tables["RSUPAC2019_R10_PARCELAS"].setPKName("ID_PARCELA")
    self.tables["RSUPAC2019_RECINTOS_SIGPAC"].setPKName("ID_RECINTO")

  def getTable(self, name):
    return self.tables[name]
    
  def write(self):
    store = self.getStore()
    trace("WRITE") 
    for recinto in self.getTable("RSUPAC2019_RECINTOS_SIGPAC").findAll():
      trace("RECINTO %s" % trace_format(recinto))
      
      parcela = self.getTable("RSUPAC2019_R10_PARCELAS").findByPK(recinto["ID_PARCELA"])
      expediente = self.getTable("RSUPAC2019_EXPEDIENTES").findByPK(parcela["ID_EXPEDIENTE"])
      
      feature = store.createNewFeature()
      feature.set("NUMEXPEDIE",expediente["NumExpediente"])
      feature.set("ID_PARCELA",parcela["ID_PARCELA"])
      feature.set("ID_RECINTO",recinto["ID_RECINTO"])
    
      feature.set("R00IDSOLIC",expediente.get("ID_Solicitante",None))
      feature.set("R00SUPERFI",expediente.get("SupDeclarada_RS_Solicitud",None))
      
      ayuda = None
      ayuda_superfifie = None
      for x in self.getTable("RSUPAC2019_AYUDA_SOL_AD").find("ID_EXPEDIENTE",expediente["ID_EXPEDIENTE"]):
        if ayuda == None:
          ayuda = x.get("Codigo_LineaAD",None)
          ayuda_superfifie = x.get("SupDeclarada_LineaAD",None)
        else:
          ayuda += ";"+x.get("Codigo_LineaAD",None)
          ayuda_superfifie += ";"+x.get("SupDeclarada_LineaAD",None)
      if ayuda!=None:
        feature.set("R00AYAD",ayuda)
      if ayuda_superfifie!=None:
        feature.set("R00AYAD_SU",ayuda_superfifie)

      ayuda = None
      for x in self.getTable("RSUPAC2019_AYUDA_SOL_AD").find("ID_EXPEDIENTE",expediente["ID_EXPEDIENTE"]):
        if ayuda == None:
          ayuda = x.get("Codigo_LineaAD",None)
        else:
          ayuda += ";"+x.get("Codigo_LineaAD",None)
      if ayuda!=None:
        feature.set("R00AYPDR",ayuda)


      feature.set("R10NUMORDE",parcela.get("PA_NumOrden",None))
      feature.set("R10SUPERFI",parcela.get("PA_SupTotalDec",None))
      feature.set("R10SISEXPL",parcela.get("PA_SistemaExplotacion",None))
      feature.set("R10PRODUCT",parcela.get("PA_Producto",None))
      feature.set("R10VARIEDA",parcela.get("PA_Variedad",None))
      feature.set("R10AAREAL",parcela.get("AA_realizada",None))

      feature.set("RECLINDECL",recinto.get("LineaDeclaracion",None))
      feature.set("RECSUPDECL",recinto.get("SupRecintoDec",None))
      feature.set("RECPROVMUN",recinto.get("ProvMuni",None))

      feature.set("RECAGREGAD",recinto.get("Agregado",None))
      feature.set("RECZONA",recinto.get("Zona",None))
      feature.set("RECPOLIGON",recinto.get("Poligono",None))
      feature.set("RECPARCELA",recinto.get("Parcela",None))
      feature.set("RECRECINTO",recinto.get("Recinto",None))
      
      feature.set("RECUSIGPAC",recinto.get("UsoSIGPAC",None))
      feature.set("RECCTRLNUE",recinto.get("CtrComplRecNuevos",None))
      feature.set("RECCAPDECL",recinto.get("CAPDeclarado",None))      
      feature.set("RECREFCATA",recinto.get("RefCatastral",None))
      feature.set("RECSIGPACS",recinto.get("SupSIGPAC",None))

      feature.set("RECZLN",recinto.get("ZLN",None))
      feature.set("RECAPRFORR",recinto.get("AprovForrajero",None))
      feature.set("RECSIE",recinto.get("SIE",None))
      
      feature.set("RECSUPNETA",recinto.get("SupNeta",None))
      feature.set("RECIDARREN",recinto.get("ID_arrendador",None))
      feature.set("RECNALMEND",recinto.get("NumAlmendros",None))
      feature.set("RECNAVELLA",recinto.get("NumAvellanos",None))
      feature.set("RECNALGARR",recinto.get("NumAlgarrobos",None))
      feature.set("RECNCASTAN",recinto.get("NumCastanos",None))
      feature.set("RECANOPLAN",recinto.get("AnoPlantFrutales",None))
      feature.set("RECSISCULH",recinto.get("SistCultivoHorticolas",None))
      feature.set("RECID_AGPC",recinto.get("ID_AGPC",None))
      feature.set("RECCOMPLET",recinto.get("Completo",None))

      ayuda = None
      for x in self.getTable("RSUPAC2019_RECINTOS_SIGPAC_AD").find("ID_RECINTO",recinto["ID_RECINTO"]):
        if ayuda == None:
          ayuda = x.get("AyudaRecinto",None)
        else:
          ayuda += ";"+x.get("AyudaRecinto",None)
      if ayuda!=None:
        feature.set("RECAYAD",ayuda)

      ayuda = None
      ayuda_superfifie = None
      for x in self.getTable("RSUPAC2019_RECINTOS_SIGPAC_PDR").find("ID_RECINTO",recinto["ID_RECINTO"]):
        if ayuda == None:
          ayuda = "%s" % x.get("LD_LineaSolicitadaPDR",None)
          ayuda_superfifie = "%s" % x.get("LD_SupSolicitadaPDR",None)
        else:
          ayuda += ";%s" % x.get("LD_LineaSolicitadaPDR",None)
          ayuda_superfifie += ";%s" % x.get("LD_SupSolicitadaPDR",None)
      if ayuda!=None:
        feature.set("RECAYPDR",ayuda)
      if ayuda_superfifie!=None:
        feature.set("RECAYPDR_S",ayuda_superfifie)
    
      feature.set("GEOMETRY",recinto.get("GEOMETRY",None))
      store.insert(feature)

      
  def insert(self, tableName, **values):
    table = self.tables[tableName]
    table.insert(values)
    if tableName == "RSUPAC2019_EXPEDIENTES":
      self.write()
      self.createInMemoryTables()


def test():
  import os
  from java.io import File
  #from addons.RSUPAC2019Converter.parsers.xmlparserfacade import create_parser
  from addons.RSUPAC2019Converter.parsers.xmlparser0 import create_parser

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
  test()
  pass
