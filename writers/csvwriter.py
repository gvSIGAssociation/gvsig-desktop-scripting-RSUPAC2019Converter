# encoding: utf-8

import gvsig

from org.gvsig.fmap.dal import DataTypes

from org.gvsig.fmap.dal import DALLocator
from org.gvsig.fmap.dal.feature import FeatureStore

import traceback

from addons.RSUPAC2019Converter.writer.rsuwriter import RSUWriter

def create_writer(status, target):
  return CSVWriter(status, target)

class CSVWriter(object):
  def __init__(self, status, target):
    RSUWriter.__init__(self, status)
    self.target = target
    self.stores = None
    self.files = None
    dataManager = DALLocator.getDataManager()
    self.server = dataManager.openServerExplorer(
          target.getExplorerName(),
          target
    )

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
    
  def getFile(self, name):
    if self.files == None:
      files = dict()
      for tableName in self.getStoreNames():
        fname = "/tmp/"+tableName+".csv"
        f = open(fname,"w")
        files[tableName] = f
      self.files = files
    return self.files[name]

  def edit(self):
    self.getFile(self.getStoreNames()[0])
    
  def finishEditing(self):
    for tableName in self.getStoreNames():
      f = self.files[tableName]
      f.close()
      
  def cancelEditing(self):
    for tableName in self.getStoreNames():
      f = self.files[tableName]
      f.close()

  def insert(self, tableName, **values):
    store = self.getStore(tableName)
    #print "### insert(%r, %r)" % (tableName, values)
   
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
    first = True
    f = self.getFile(tableName)
    for attrdesc in featureType:
      if attrdesc.getType()==DataTypes.GEOMETRY or attrdesc.isComputed():
        continue
      value = feature.get(attrdesc.getName())
      if first:
        first=False
      else:
        f.write(";")
      if value == None:
        continue
      if attrdesc.getDataType().isNumeric():
        f.write("%s" %  value)
      else:
        f.write("\"%s\"" % repr(value))
    f.write("\n")
    
def main(*args):
    pass
