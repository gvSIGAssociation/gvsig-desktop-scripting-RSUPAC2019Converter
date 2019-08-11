# encoding: utf-8

import gvsig

from org.gvsig.fmap.dal import DataTypes

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal.feature import FeatureStore
from org.gvsig.tools import ToolsLocator

import traceback

from addons.RSUPAC2019Converter.writers.rsuwriter import RSUWriter
from addons.RSUPAC2019Converter.trace import trace, trace_format, trace_remove

from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_EXPEDIENTES
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_EXPLOTACIONES
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_ORIGEN_ANIMALES
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_AYUDA_SOL_AD
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_AYUDA_SOL_PDR
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_R10_PARCELAS
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_AD
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_PDR
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_AS
from addons.RSUPAC2019Converter.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_CH

from addons.RSUPAC2019Converter.createviews import createViews

VIEWS = {
    "RSUPAC2019_RSU_PARCELAS_RECINTOS" : """CREATE VIEW RSUPAC2019_RSU_PARCELAS_RECINTOS AS
SELECT
concat( RSUPAC2019_EXPEDIENTES."NumExpediente", '/', RSUPAC2019_R10_PARCELAS."ID_PARCELA", '/', RSUPAC2019_RECINTOS_SIGPAC."ID_RECINTO" ) as ID ,
RSUPAC2019_EXPEDIENTES.*,
RSUPAC2019_R10_PARCELAS."ID_PARCELA",
RSUPAC2019_RECINTOS_SIGPAC."ID_RECINTO",
RSUPAC2019_R10_PARCELAS."PA_NumOrden",
RSUPAC2019_R10_PARCELAS."PA_Ciclo",
RSUPAC2019_R10_PARCELAS."AA_realizada",
RSUPAC2019_R10_PARCELAS."PA_SupTotalDec",
RSUPAC2019_R10_PARCELAS."PA_SistemaExplotacion",
RSUPAC2019_R10_PARCELAS."PA_Producto",
RSUPAC2019_R10_PARCELAS."PA_Variedad",
RSUPAC2019_R10_PARCELAS."ProdEcologica",
RSUPAC2019_R10_PARCELAS."TipSemilla",
RSUPAC2019_RECINTOS_SIGPAC."LineaDeclaracion",
RSUPAC2019_RECINTOS_SIGPAC."SupRecintoDec",
RSUPAC2019_RECINTOS_SIGPAC."ProvMuni",
RSUPAC2019_RECINTOS_SIGPAC."Agregado",
RSUPAC2019_RECINTOS_SIGPAC."Zona",
RSUPAC2019_RECINTOS_SIGPAC."Poligono",
RSUPAC2019_RECINTOS_SIGPAC."Parcela",
RSUPAC2019_RECINTOS_SIGPAC."Recinto",
RSUPAC2019_RECINTOS_SIGPAC."RefCatastral",
RSUPAC2019_RECINTOS_SIGPAC."SupSIGPAC",
RSUPAC2019_RECINTOS_SIGPAC."UsoSIGPAC",
RSUPAC2019_RECINTOS_SIGPAC."CtrComplRecNuevos",
RSUPAC2019_RECINTOS_SIGPAC."CAPDeclarado",
RSUPAC2019_RECINTOS_SIGPAC."SupNeta",
RSUPAC2019_RECINTOS_SIGPAC."RegTenencia",
RSUPAC2019_RECINTOS_SIGPAC."Extran_Arrendador",
RSUPAC2019_RECINTOS_SIGPAC."ID_arrendador",
RSUPAC2019_RECINTOS_SIGPAC."CC_No_SIGPAC",
RSUPAC2019_RECINTOS_SIGPAC."PastoComunal",
RSUPAC2019_RECINTOS_SIGPAC."NombrePasto",
RSUPAC2019_RECINTOS_SIGPAC."CodPasto",
RSUPAC2019_RECINTOS_SIGPAC."ZLN",
RSUPAC2019_RECINTOS_SIGPAC."AprovForrajero",
RSUPAC2019_RECINTOS_SIGPAC."Observaciones",
RSUPAC2019_RECINTOS_SIGPAC."SIE",
RSUPAC2019_RECINTOS_SIGPAC."NumAlmendros",
RSUPAC2019_RECINTOS_SIGPAC."NumAvellanos",
RSUPAC2019_RECINTOS_SIGPAC."NumAlgarrobos",
RSUPAC2019_RECINTOS_SIGPAC."NumCastanos",
RSUPAC2019_RECINTOS_SIGPAC."AnoPlantFrutales",
RSUPAC2019_RECINTOS_SIGPAC."SistCultivoHorticolas",
RSUPAC2019_RECINTOS_SIGPAC."Destino",
RSUPAC2019_RECINTOS_SIGPAC."Nombre_AGPC",
RSUPAC2019_RECINTOS_SIGPAC."Extran_AGPC",
RSUPAC2019_RECINTOS_SIGPAC."ID_AGPC",
RSUPAC2019_RECINTOS_SIGPAC."ProductoCS",
RSUPAC2019_RECINTOS_SIGPAC."VariedadCS",
RSUPAC2019_RECINTOS_SIGPAC."TipSemillaCS",
RSUPAC2019_RECINTOS_SIGPAC."DestinoCS",
RSUPAC2019_RECINTOS_SIGPAC."CoordX_Centroide",
RSUPAC2019_RECINTOS_SIGPAC."CoordY_Centroide",
RSUPAC2019_RECINTOS_SIGPAC."Completo",
RSUPAC2019_RECINTOS_SIGPAC."GEOMETRY"
FROM RSUPAC2019_EXPEDIENTES
INNER JOIN RSUPAC2019_R10_PARCELAS ON RSUPAC2019_EXPEDIENTES."ID_EXPEDIENTE" = RSUPAC2019_R10_PARCELAS."ID_EXPEDIENTE"
INNER JOIN RSUPAC2019_RECINTOS_SIGPAC ON RSUPAC2019_R10_PARCELAS."ID_PARCELA" = RSUPAC2019_RECINTOS_SIGPAC."ID_PARCELA"
"""

}

VIEWS = {}

def create_writer(status, target):
  return DBWriter(status, target)

def workspace_drop(ws):
  if not ws.existsTable(ws.TABLE_RESOURCES):
      ws.dropTable(ws.TABLE_RESOURCES)
  if not ws.existsTable(ws.TABLE_CONFIGURATION):
      ws.dropTable(ws.TABLE_CONFIGURATION)
  if not ws.existsTable(ws.TABLE_REPOSITORY):
      ws.dropTable(ws.TABLE_REPOSITORY)


class DBWriter(RSUWriter):
  def __init__(self, status, target):
    RSUWriter.__init__(self, status)
    dataManager = DALLocator.getDataManager()
    self.server = dataManager.openServerExplorer(
          target.getExplorerName(),
          target
    )
    self.stores = None

  def getStoreNames(self):
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
        
  def getStore(self, name):
    if self.stores == None:
      stores = dict()
      dataManager = DALLocator.getDataManager()
      for tableName in self.getStoreNames():
        self.status.message("Abriendo tabla ("+tableName+")")
        parameters = self.server.get(tableName)
        store = dataManager.openStore(parameters.getProviderName(),parameters)
        stores[tableName] = store
      self.stores = stores      
    return self.stores[name]

  def create(self):
    dataManager = DALLocator.getDataManager()
    workspace = dataManager.createDatabaseWorkspaceManager(self.server.getParameters())
    workspace.create("RSUPAC2019","RSU PAC 2019 (db)")

    for tableName, add_attributes in (
      ("RSUPAC2019_EXPEDIENTES",add_fields_RSUPAC2019_EXPEDIENTES), 
      ("RSUPAC2019_EXPLOTACIONES",add_fields_RSUPAC2019_EXPLOTACIONES), 
      ("RSUPAC2019_ORIGEN_ANIMALES",add_fields_RSUPAC2019_ORIGEN_ANIMALES), 
      ("RSUPAC2019_AYUDA_SOL_AD",add_fields_RSUPAC2019_AYUDA_SOL_AD), 
      ("RSUPAC2019_AYUDA_SOL_PDR",add_fields_RSUPAC2019_AYUDA_SOL_PDR), 
      ("RSUPAC2019_R10_PARCELAS",add_fields_RSUPAC2019_R10_PARCELAS), 
      ("RSUPAC2019_RECINTOS_SIGPAC",add_fields_RSUPAC2019_RECINTOS_SIGPAC), 
      ("RSUPAC2019_RECINTOS_SIGPAC_AD",add_fields_RSUPAC2019_RECINTOS_SIGPAC_AD), 
      ("RSUPAC2019_RECINTOS_SIGPAC_PDR",add_fields_RSUPAC2019_RECINTOS_SIGPAC_PDR), 
      ("RSUPAC2019_RECINTOS_SIGPAC_AS",add_fields_RSUPAC2019_RECINTOS_SIGPAC_AS), 
      ("RSUPAC2019_RECINTOS_SIGPAC_CH",add_fields_RSUPAC2019_RECINTOS_SIGPAC_CH), 
      ):
      self.status.message("Creando "+tableName)
      params = self.server.getAddParameters(tableName)
      ft = params.getDefaultFeatureType()
      add_attributes(ft)
      self.server.add(tableName, params, False)
      
    for tableName in self.getStoreNames():
      self.status.message("Actualizando espacio de trabajo ("+tableName+")")
      params = self.server.get(tableName)
      workspace.writeStoresRepositoryEntry(tableName, params)

    for sql in VIEWS.itervalues():
      self.server.execute(sql)
    
  def drop(self):
    for viewName in VIEWS.iterkeys():
      s = 'DROP VIEW IF EXISTS "%s"' % viewName
      trace(s)
      self.server.execute(s)

    for tableName in self.getStoreNames():
      self.status.message("Eliminando "+tableName)
      try:
        params = self.server.get(tableName)
        self.server.remove(params)
      except:
        pass
    self.status.message("Eliminando workspace")
    dataManager = DALLocator.getDataManager()
    workspace = dataManager.createDatabaseWorkspaceManager(self.server.getParameters())
    
    #workspace.drop()
    workspace_drop(workspace)

  def edit(self):
    for tableName in self.getStoreNames():
      store = self.getStore(tableName)
      if not (store.isEditing() or store.isAppending()):
        trace("BEGIN EDIT %s" % tableName)
        store.edit(FeatureStore.MODE_APPEND)
    
  def finishEditing(self):
    for tableName in self.getStoreNames():
      store = self.getStore(tableName)
      if store.isEditing() or store.isAppending():
        trace("END EDIT %s" % tableName)
        store.finishEditing()
      
  def cancelEditing(self):
    for tableName in self.getStoreNames():
      try:
        store = self.getStore(tableName)
        if store.isEditing() or store.isAppending():
          trace("CANCEL EDIT %s" % tableName)
          store.cancelEditing()
      except:
        print "Error cancelEditing table '"+tableName+"'."
        traceback.print_exc()

  def insert(self, tableName, **values):
    store = self.getStore(tableName)
    trace("INSERT INTO %s VALUES %s" % (tableName,trace_format(values)))
   
    featureType = store.getDefaultFeatureType()
    feature = store.createNewFeature()
    for name, value in values.iteritems():
      attrdesc = featureType.get(name)
      if attrdesc == None:
        raise Exception("No existe el campo %r in la tabla %r" % (name, tableName))
        #print "ERROR: No existe el campo %r in la tabla %r" % (name, tableName)
        #continue 
      if value!=None and attrdesc.getType()==DataTypes.BOOLEAN:
        if value.lower()=="s":
          feature.set(name,True)
          continue
        elif value.lower()=="n":
          feature.set(name,False)
          continue
      feature.set(name,value)
    store.insert(feature)
 

def main(*args):
  pass
