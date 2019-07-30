# encoding: utf-8

import gvsig

from org.gvsig.fmap.dal import DataTypes

from org.gvsig.fmap.dal import DALLocator

import traceback

class DBWriter(object):
  def __init__(self, server, status):
    self.server = server
    self.status = status
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
    
  def edit(self):
    for tableName in self.getStoreNames():
      store = self.getStore(tableName)
      print "### edit(%r)" % tableName
      if not store.isEditing():
        store.edit()
      
  def finishEditing(self):
    for tableName in self.getStoreNames():
      store = self.getStore(tableName)
      print "### finishEditing(%r)" % tableName
      if store.isEditing():
        store.finishEditing()

  def cancelEditing(self):
    for tableName in self.getStoreNames():
      try:
        store = self.getStore(tableName)
        print "### cancelEditing(%r)" % tableName
        if store.isEditing():
          store.cancelEditing()
      except:
        print "Error cancelEditing table '"+tableName+"'."
        traceback.print_exc()

  def insert(self, tableName, **values):
    store = self.getStore(tableName)
    print "### insert(%r, %r)" % (tableName, values)
    
    featureType = store.getDefaultFeatureType()
    f = store.createNewFeature()
    for name, value in values.iteritems():
      attrdesc = featureType.get(name)
      if attrdesc == None:
        raise Exception("No existe el campo %r in la tabla %r" % (name, tableName))
      if value!=None and attrdesc.getType()==DataTypes.BOOLEAN:
        if value.lower()=="s":
          f.set(name,True)
          continue
        elif value.lower()=="n":
          f.set(name,False)
          continue
      f.set(name,value)
    store.insert(f)
    store.commitChanges()
    
def main(*args):
    pass
