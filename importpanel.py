# encoding: utf-8

import gvsig

from gvsig import getResource
from gvsig.libs.formpanel import FormPanel
from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.dal.swing import DALSwingLocator 
from org.gvsig.tools.swing.api import ToolsSwingLocator
from java.lang import Thread
from org.gvsig.tools.observer import Observer

from addons.RSUPAC2019Importer.importprocess import createImportProcess


class ImportDialog(FormPanel, Observer):
  def __init__(self):
    FormPanel.__init__(self,getResource(__file__,"importpanel.xml"))
    self.sourcePicker = None
    self.targetPicker = None
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
    self.targetPicker = dataSwingManager.createJDBCConnectionPickerController(
            self.cboTarget,
            self.btnTarget
    )
    self.targetPicker.addChangeListener(self.doInputsChanged)
    
    self.taskStatusController = taskManager.createTaskStatusController(
      self.lblTaskTitle,
      self.lblTaskMessage,
      self.pgbTaskProgress
    )
    self.btnImport.setEnabled(False)
    self.setVisibleTaskStatus(False)
    self.setPreferredSize(500,200)

  def setVisibleTaskStatus(self, visible):
    self.lblTaskTitle.setVisible(visible)
    self.pgbTaskProgress.setVisible(visible)
    self.lblTaskMessage.setVisible(visible)
    
  def doInputsChanged(self, *args):
    source = self.sourcePicker.get()
    target = self.targetPicker.get()
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
        
    process = createImportProcess(
      self.sourcePicker.get(),
      self.targetPicker.get(),
      self.status
    )
    th = Thread(process, "SRUPAC_2019_import")
    th.start()

def showImportPanel():
  panel = ImportDialog()
  panel.showWindow("SRU PAC 2019 Importador")

def main(*args):
  showImportPanel()
  
