# encoding: utf-8

import gvsig

import traceback

from java.lang import Runnable
from java.lang import Thread
import java.lang.Exception 

from org.gvsig.fmap.dal import DALLocator

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


class ImportProcess(Runnable):
  def __init__(self, source, target, status):
    self.source = source
    self.target = target
    self.status = status

  def run(self):
    try:
      count = 12+12
      
      self.status.setRangeOfValues(0,count)
      self.status.setCurValue(0)
      
      dataManager = DALLocator.getDataManager()
      self.workspace = dataManager.createDatabaseWorkspaceManager(self.target)
      self.server = dataManager.openServerExplorer(
          self.target.getExplorerName(),
          self.target
      )

      self.status.message("Creando espacio de trabajo")
      self.workspace.create("SRUPAC2019","SRU PAC 2019 (db)")

      self.createTables()
      self.addTablesToWorkspace()

      #
      # Aqui:
      # - Crear el escritor en BBDD
      # - Crear el lector del XML 
      # - que parsee 
      #
      # Por ejemplo:
      #
      # dbwriter = SRUPACDBWriter(self.server, self.status)
      # xmlreader = SRUPACXMLReader()
      # xmlreader.parse(dbwriter)
      #
      # El SRUPACDBWriter y SRUPACXMLReader los pasaria a modulos aparte 
      # y arriba pondria los imports
      # Cuidado en ellos que no estamos en el thread de swing, no podemos
      # tocar el GUI.
      #
      # En el dbwriter puedes obtener los stores con:
      # params = self.server.get("RSUPAC2019_R10_PARCELAS")
      # store = dataManager.openStore(params.getProviderName(),params) 
      #
              
      self.status.message("Importacion completada")
      self.status.terminate()

    except java.lang.Exception, ex:
      print "Error creating tables", str(ex)
      traceback.print_exc()
      self.status.message("ERROR. " + self.status.getTitle())
      self.status.abort()

    except Exception, ex:
      print "Error creating tables", str(ex)
      traceback.print_exc()
      
      self.status.message("ERROR. " + self.status.getTitle())
      self.status.abort()
    except:
      print "Error creating tables"
      traceback.print_exc()
      self.status.message("ERROR. " + self.status.getTitle())
      self.status.abort()
    finally:
      pass

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
      ):
      self.status.message("Actualizando espacio de trabajo ("+tableName+")")
      self.status.incrementCurrentValue()
      params = self.server.get(tableName)
      self.workspace.writeStoresRepositoryEntry(tableName, params)

def createImportProcess(source, target, status):
  return ImportProcess(source, target, status)
  
def main(*args):
    pass
