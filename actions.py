# encoding: utf-8

import gvsig
from gvsig import getResource

from java.io import File
from org.gvsig.andami import PluginsLocator
from org.gvsig.app import ApplicationLocator
from org.gvsig.scripting.app.extension import ScriptingExtension
from org.gvsig.tools import ToolsLocator
from org.gvsig.tools.swing.api import ToolsSwingLocator

from addons.RSUPAC2019Converter.importpanel import showImportPanel

class RSUPAC2019ConverterExtension(ScriptingExtension):
  def __init__(self):
    pass

  def canQueryByAction(self):
    return False

  def isEnabled(self,action=None):
    return True

  def isVisible(self,action=None):
    return True
    
  def execute(self,actionCommand, *args):
    actionCommand = actionCommand.lower()
    if actionCommand == "rsupac2019-converter-show":
      self.importData()
              
  def importData(self):
    showImportPanel()
    
def selfRegister():
  application = ApplicationLocator.getManager()

  #
  # Registramos las traducciones
  i18n = ToolsLocator.getI18nManager()
  i18n.addResourceFamily("text",File(getResource(__file__,"i18n")))

  #
  # Registramos los iconos en el tema de iconos
  iconTheme = ToolsSwingLocator.getIconThemeManager().getCurrent()
  icon = File(getResource(__file__,"images","rsupac2019-converter-show.png")).toURI().toURL()
  iconTheme.registerDefault("scripting.RSUPAC2019ConverterExtension", "action", "rsupac2019-converter-show", None, icon)

  #
  # Creamos la accion 
  actionManager = PluginsLocator.getActionInfoManager()
  extension = RSUPAC2019ConverterExtension()
  
  action = actionManager.createAction(
    extension, 
    "rsupac2019-converter-show", # Action name
    "Conversor RSU-PAC 2019", # Text
    "rsupac2019-converter-show", # Action command
    "rsupac2019-converter-show", # Icon name
    None, # Accelerator
    650700600, # Position 
    "_Show_the_RSUPAC_2019_converter_tool" # Tooltip
  )
  action = actionManager.registerAction(action)
  application.addMenu(action, "tools/RSU PAC 2019/Conversor")
  
