# encoding: utf-8

import gvsig

import os.path

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.dal.swing import DALSwingLocator 
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.lang import Thread
from org.gvsig.tools.observer import Observer
from java.io import File
from javax.swing import ButtonGroup


from addons.RSUPAC2019Importer.importprocess import createImportProcess

from addons.RSUPAC2019Importer.parsers.xmlparser0 import create_parser
#from addons.RSUPAC2019Importer.parsers.xmlparser1 import XmlParser1 as RSUParser
#from addons.RSUPAC2019Importer.parsers.xmlparserfacade import XMLParserFacade as RSUParser

from addons.RSUPAC2019Importer.writers import dbwriter
reload(dbwriter)

from addons.RSUPAC2019Importer.writers.dbwriter import create_writer as create_writer_db
#from addons.RSUPAC2019Importer.writers.csvwriter import CSVWriter
from addons.RSUPAC2019Importer.writers.shpwriter import create_writer as create_writer_shp
from addons.RSUPAC2019Importer.writers.writerfacade import create_writer as create_writer_facade


class ImportDialog(FormPanel, Observer):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"importpanel.xml"))
    self.sourcePicker = None
    self.targetPickerDb = None
    self.targetPickerShp = None
    self.taskStatusController = None
    self.status = None
    self.initComponents()

  def initComponents(self):
    i18n = ToolsLocator.getI18nManager()
    toolsSwingManager = ToolsSwingLocator.getToolsSwingManager()
    dataSwingManager = DALSwingLocator.getSwingManager()
    taskManager = ToolsSwingLocator.getTaskStatusSwingManager()

    self.sourcePicker = toolsSwingManager.createFilePickerController(
      self.txtSource, 
      self.btnSource
    )
    self.sourcePicker.addChangeListener(self.doInputsChanged)
    self.sourcePicker.coerceAndSet(
      getResource(__file__,"datos", "test","RSU_PAC_2019_muestra.xml")
    )
    self.targetPickerDb = dataSwingManager.createJDBCConnectionPickerController(
            self.cboTarget,
            self.btnTarget
    )
    self.targetPickerDb.addChangeListener(self.doInputsChanged)
    
    self.targetPickerShp = toolsSwingManager.createFilePickerController(
      self.txtTargetShape, 
      self.btnTargetShappe
    )
    self.targetPickerShp.addChangeListener(self.doInputsChanged)
    
    self.taskStatusController = taskManager.createTaskStatusController(
      self.lblTaskTitle,
      self.lblTaskMessage,
      self.pgbTaskProgress
    )

    self.btgTargets = ButtonGroup()
    self.btgTargets.add(self.rdbDDBB)
    self.btgTargets.add(self.rdbShape)

    self.rdbShape.setSelected(True)
    
    #self.btnImport.setEnabled(False)
    self.setVisibleTaskStatus(False)
    
    self.doInputsChanged()
    self.setPreferredSize(750,290)

  def setVisibleTaskStatus(self, visible):
    self.lblTaskTitle.setVisible(visible)
    self.pgbTaskProgress.setVisible(visible)
    self.lblTaskMessage.setVisible(visible)

  def rdbShape_click(self,*args):
    self.doInputsChanged()
    
  def rdbDDBB_click(self,*args):
    self.doInputsChanged()
    
  def doInputsChanged(self, *args):
    source = self.sourcePicker.get()
    if self.rdbDDBB.isSelected():
      target = self.targetPickerDb.get()    
      self.targetPickerDb.setEnabled(True)
      self.targetPickerShp.setEnabled(False)
      
    elif self.rdbShape.isSelected():
      target = self.targetPickerShp.get()
      self.targetPickerDb.setEnabled(False)
      self.targetPickerShp.setEnabled(True)
      
    if target == None or source == None:
      self.btnImport.setEnabled(False)
    else:
      self.btnImport.setEnabled(True)
      
  def update(self, observable, notification):
    if self.status == None:
      return
    if not self.status.isRunning():
      self.btnClose.setEnabled(True)
      if self.status.isAborted():
        self.btnImport.setEnabled(True)
      else:
        self.setVisibleTaskStatus(False)
        self.btnImport.setEnabled(False)
    
  def btnImport_click(self, *args):
    taskManager = ToolsLocator.getTaskStatusManager()
    self.status = taskManager.createDefaultSimpleTaskStatus("SRU PAC")
    self.status.addObserver(self)
    self.taskStatusController.bind(self.status)
    self.setVisibleTaskStatus(True)
    self.btnClose.setEnabled(False)
    self.btnImport.setEnabled(False)
    
    if self.rdbDDBB.isSelected():
      writer = create_writer_db(self.status, self.targetPickerDb.get())
    elif self.rdbShape.isSelected():
      writer = create_writer_shp(self.status, self.targetPickerShp.get())
    else:
      return
    #writer = create_writer_facade(self.status)
    
    parser = create_parsers(self.status, self.sourcePicker.get())
    
    process = createImportProcess(
      parser,
      writer,
      self.status,
      create=True
    )
    th = Thread(process, "SRUPAC_2019_import")
    th.start()

def showImportPanel():
  panel = ImportDialog()
  panel.showWindow("RSU PAC 2019 Conversor")


def create_parsers(status, xmlfile):
  parsers = list()
  fname = xmlfile.getAbsolutePath()
  if fname.endswith("_001.XML"):
    base = fname[:-8]
    #print "base %r" % base
    for i in range(1,20):
      fname = "%s_%03d.XML" % (base,i)
      #print "fname %s" % fname
      if not os.path.exists(fname):
        break
      parser = create_parser(status, File(fname))
      parsers.append(parser)
  else:
    parser = create_parser(status, File(fname))
    parsers.append(parser)
  return parsers
  
def test():
  
  fname = r"C:\Users\D73553626V\Desktop\gvSIG-desktop-2.5.0-2918-testing-win-x86_64\datos\BDA_RSU_PAC19_1723072019_001.XML"
  taskManager = ToolsLocator.getTaskStatusManager()
  status = taskManager.createDefaultSimpleTaskStatus("SRU PAC")

  parsers = create_parsers(status, File(fname))
  print parsers
    
def main(*args):
  showImportPanel()
  #test()
  
  
