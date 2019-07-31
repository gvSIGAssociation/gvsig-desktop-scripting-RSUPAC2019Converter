# encoding: utf-8

import gvsig

import traceback

from java.lang import Runnable
from java.lang import Thread
import java.lang.Exception 

from org.gvsig.fmap.dal import DALLocator

from addons.RSUPAC2019Importer.dbwriter import DBWriter

from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_EXPEDIENTES
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_EXPLOTACIONES
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_ORIGEN_ANIMALES
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_AYUDA_SOL_AD
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_AYUDA_SOL_PDR
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_R10_PARCELAS
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_AD
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_PDR
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_AS
from addons.RSUPAC2019Importer.createtables_RSUPAC import add_fields_RSUPAC2019_RECINTOS_SIGPAC_CH

from addons.RSUPAC2019Importer.createviews import createViews

from addons.RSUPAC2019Importer.parserRSU import RSUGrafParser
from addons.RSUPAC2019Importer.xmlreaderfacade import XMLReaderFacade    

class ImportProcess(Runnable):
  def __init__(self, source, target, status):
    self.source = source
    self.target = target
    self.status = status
    
    self.server = None
    self.dbwriter = None
    self.xmlreader = None

  def run(self):
    try:
      dataManager = DALLocator.getDataManager()
      self.workspace = dataManager.createDatabaseWorkspaceManager(self.target)
      self.server = dataManager.openServerExplorer(
          self.target.getExplorerName(),
          self.target
      )
      self.xmlreader = RSUGrafParser(self.status)
      #self.xmlreader = XMLReaderFacade(self.status)

      count = 12+12+self.xmlreader.getCount(self.source)
      
      self.status.setRangeOfValues(0,count)
      self.status.setCurValue(0)

      self.status.message("Creando espacio de trabajo")
      self.workspace.create("RSUPAC2019","RSU PAC 2019 (db)")

      self.createTables()
      createViews(self.server)
      self.addTablesToWorkspace()

      self.status.message("Cargando...")
      self.dbwriter = DBWriter(self.server, self.status)

      self.dbwriter.edit()
      self.xmlreader.parse(self.dbwriter, self.source)
      self.dbwriter.finishEditing()
      
      self.status.message("Importacion completada")
      self.status.terminate()

    except:
      print "Error importing data"
      traceback.print_exc()
      self.status.setTitle("ERROR. " + self.status.getTitle())
      self.status.abort()
      if self.dbwriter!=None:
        self.dbwriter.cancelEditing()

    finally:
      if self.xmlreader!=None:
        self.xmlreader.close()
      

  def createTables(self):
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
      self.status.incrementCurrentValue()

  def addTablesToWorkspace(self):
    for tableName in (
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
      "RSUPAC2019_RSU_PARCELAS_RECINTOS",
      ):
      self.status.message("Actualizando espacio de trabajo ("+tableName+")")
      self.status.incrementCurrentValue()
      params = self.server.get(tableName)
      self.workspace.writeStoresRepositoryEntry(tableName, params)

def createImportProcess(source, target, status):
  return ImportProcess(source, target, status)

def main(*args):
    pass
