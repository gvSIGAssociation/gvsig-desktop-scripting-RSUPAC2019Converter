# encoding: utf-8

import gvsig

from org.gvsig.fmap.geom.aggregate import MultiPolygon
from org.gvsig.scripting.app.extension import ScriptingUtils
from org.gvsig.fmap.geom import GeometryUtils
from org.xmlpull.v1 import XmlPullParser
from java.io import File
from org.xmlpull.v1 import XmlPullParserException
from org.xmlpull.v1 import XmlPullParserFactory
from java.io import File, FileInputStream
from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.crs import CRSFactory

"""
Tablas a crear en el esquema "public":
- RSUPAC2019_EXPEDIENTES
- RSUPAC2019_EXPLOTACIONES
- RSUPAC2019_ORIGEN_ANIMALES
- RSUPAC2019_AYUDA_SOL_AD
- RSUPAC2019_AYUDA_SOL_PDR

- RSUPAC2019_R10_PARCELAS
- RSUPAC2019_RECINTOS_SIGPAC (R10_Parcelas/LD_RecintosSIGPAC)
- RSUPAC2019_RECINTOS_SIGPAC_AD (R10_Parcelas/LD_RecintosSIGPAC/LD_Linea_AyudaSolAD)
- RSUPAC2019_RECINTOS_SIGPAC_PDR (R10_Parcelas/LD_RecintosSIGPAC/LD_Linea_AyudaSolPDR)
- RSUPAC2019_RECINTOS_SIGPAC_AS (R10_Parcelas/LD_RecintosSIGPAC/AyudaSecundario)
- RSUPAC2019_RECINTOS_SIGPAC_CH (R10_Parcelas/LD_RecintosSIGPAC/CultivosHorticolas)

"""

class RSUInsertFeatures(object):
  def __init__(self):
    self.m = 0
    pass
    
  def insert(self, nombretabla, **params):
    #if nombretabla == "RSUPAC2019_RECINTOS_SIGPAC_AD":
    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #print self.m, "@@@@@@@ INSERT IN ", nombretabla, " VALUES:",
    self.m +=1
    #pp.pprint(params)

    print "@@@@@@@ INSERT IN ", nombretabla #, " VALUES:", params
    pass
    
class RSUGrafParser(object):
  
  def __init__(self, status=None):
    self.status = status
    self.xml = None
    factory = XmlPullParserFactory.newInstance(ToolsLocator.getInstance().getXmlPullParserFactoryClassNames(),None)
    self.parser = factory.newPullParser()
    self.dbwriter = RSUInsertFeatures()
    self.count = 0
    self.initValues()
    self.n = 1 # Safety while

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
    
  def rewind(self):
    factory = XmlPullParserFactory.newInstance(ToolsLocator.getInstance().getXmlPullParserFactoryClassNames(),None)
    self.parser = factory.newPullParser()
    self.initValues()
    self.open()
        
  def isDone(self):
    return self.done

  def open(self):
    ScriptingUtils.log(ScriptingUtils.WARN, "Loading file xml "+ self.fname.getName())
    self.resource = FileInputStream(self.fname)
    self.parser.setInput(self.resource, None);
    ScriptingUtils.log(ScriptingUtils.WARN, "File loaded.")
    self.initValues()
    self.readInitValues()

  def readInitValues(self):
    self.parser.nextTag()
    self.parser.require(XmlPullParser.START_TAG, None, "Expedientes_RSU")
    self.parser.nextTag()

  def initValues(self):
    # Reset and init values
    self.done = False
    self.actual_RSU_NumExpediente = "xxx"
    self.num_Explotaciones = 0
    self.num_OrigenAnimales = 0
    self.num_Linea_AyudaSolAD = 0
    self.num_Linea_AyudaSolPDR = 0
    self.num_R10_Parcelas = 0 #id especial
    self.num_LD_RecintoSIGPAC = 0
    self.num_LD_Linea_AyudaSolAD = 0
    self.num_LD_Linea_AyudaSolPDR = 0
    self.num_AyudaSecundario = 0
    self.num_CultivosHorticolas = 0
    self.num_PA_NumOrden = 999
    self.ID_PARCELA = 0
  
  def checkAndTransformWKT(self, wkt, srid):
    geom = None
    if wkt!=None:
      if "EMPTY" in wkt:
        #ScriptingUtils.log(ScriptingUtils.WARN, "La geometria no es valida en %s:%s, el poligono esta vacio" % (self.num_expediente, self.num_parcela))
        pass
      else:
        geom = GeometryUtils.createFrom(wkt, "EPSG:4326")#+srid)
        if geom!=None and not geom.isValid():
          #status = geom.getValidationStatus()
          #msg = status.getMessage()
          #ScriptingUtils.log(ScriptingUtils.WARN, "La geometria no es valida en %s:%s, %s" % (self.num_expediente, self.num_parcela, msg))
          geom = None
      
      if geom!=None and not isinstance(geom,MultiPolygon):
        geom = geom.toPolygons()
      if geom!=None:
        geom.setProjection(CRSFactory.getCRS("EPSG:4326"))#"+srid))
    return geom

  def dicR10_Parcelas(self):
    dic = {"ID_PARCELA": 999, "NumExpediente":self.actual_RSU_NumExpediente}
    self.num_R10_Parcelas+=1
    return dic
    
  def parseRSU(self):
    ## Start with expediente
    self.parser.require(XmlPullParser.START_TAG, "", "RSU")
    dicValues = {} ### VALORES DEL RSU
    self.parser.nextTag()
    while True:
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU": # Cuando siguen tags despues de unbounded
        break
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R00_Solicitante":
        self.parseR00_Solicitante(dicValues)
        self.parser.require(XmlPullParser.END_TAG, "", "R00_Solicitante")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R00_Solicitud":
        self.parseR00_Solicitud(dicValues)
        self.parser.require(XmlPullParser.END_TAG, "", "R00_Solicitud")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R10_Parcelas":
        self.parseR10_Parcelas()
        self.parser.require(XmlPullParser.END_TAG, "", "R10_Parcelas")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R11_Socios":
        self.parseUntilClose("R11_Socios")
        self.parser.require(XmlPullParser.END_TAG, "", "R11_Socios")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R12_Entidades":
        self.parseUntilClose("R12_Entidades")
        self.parser.require(XmlPullParser.END_TAG, "", "R12_Entidades")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R30_AnimalesPDR":
        self.parseUntilClose("R30_AnimalesPDR")
        self.parser.require(XmlPullParser.END_TAG, "", "R30_AnimalesPDR")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R40_ApiculturaPDR":
        self.parseUntilClose("R40_ApiculturaPDR")
        self.parser.require(XmlPullParser.END_TAG, "", "R40_ApiculturaPDR")
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R50_EntidadesAsoc":
        self.parseUntilClose("R50_EntidadesAsoc")
        self.parser.require(XmlPullParser.END_TAG, "", "R50_EntidadesAsoc")
      else:
        #print "last else insertActualTag: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
        self.insertActualTag(dicValues)
        if self.actual_RSU_NumExpediente == "xxx" and "NumExpediente" in dicValues:
          self.actual_RSU_NumExpediente = dicValues["NumExpediente"]
        
      # Ending while setting new
      # Tiene que llegar el tag de cierre
      self.parser.nextTag()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="RSU":
        dicValues = fixFieldNames(dicValues)
        #print "Expediente: ", self.actual_RSU_NumExpediente, " count: ", self.n
        self.n+=1
        self.insertFactory.insert("RSUPAC2019_EXPEDIENTES", **dicValues)
        self.actual_RSU_NumExpediente =  "xxx"
        break

  def parseUntilClose(self, nameTag):
    self.parser.nextTag()
    while True:
      self.parser.next()
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()==nameTag:
        break
        
  def parseComplexType(self, nameTag, dicValues):
    self.parser.nextTag()
    while True:
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()==nameTag:
        break
        
      
  def parseR00_Solicitante(self, dicValues):
    self.parser.nextTag()
    while True:
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="R00_Solicitante":
        break

  def parseR00_Solicitud(self, dicValues):
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      if checkStart and parserTagName=="Conyuge":
        self.parseComplexType("Conyuge", dicValues)
      elif checkStart and parserTagName=="Representante":
        self.parseComplexType("Representante", dicValues)
      elif checkStart and parserTagName=="RespJuridica":
        self.parseComplexType("RespJuridica", dicValues)
      elif checkStart and parserTagName=="JefeExplotacion":
        self.parseComplexType("JefeExplotacion", dicValues)
      elif checkStart and parserTagName=="DatosBancarios":
        self.parseComplexType("DatosBancarios", dicValues)
      elif checkStart and parserTagName=="OtrosDatos":
        self.parseOtrosDatos(dicValues)
      elif checkStart and self.parser.getName()=="JefeExplotacion":
        self.parseComplexType("JefeExplotacion", dicValues)
      elif checkStart and self.parser.getName()=="ResumenSol":
        self.parseResumenSol(dicValues)
      else:
        self.insertActualTag(dicValues)

      self.parser.nextTag()
      statusBlock = self.endBlockCheck("R00_Solicitud")
      if statusBlock == True: break
        
  def parseResumenSol(self, dicValues):
    self.parser.nextTag()
    while True:
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Linea_AyudaSolAD":
        self.parseLinea_AyudaSolAD()
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Linea_AyudaSolPDR":
        self.parseLinea_AyudaSolPDR()
      else:
        self.insertActualTag(dicValues)

      self.parser.nextTag()
      statusBlock = self.endBlockCheck("ResumenSol")
      if statusBlock == True: break
      
  def parseOtrosDatos(self, dicValues):
    self.parser.nextTag()
    while True:
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Explotaciones":
        self.parseExplotaciones()
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="OrigenAnimales":
        self.parseOrigenAnimales()
      else:
        self.insertActualTag(dicValues)
      self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="OtrosDatos":
        break
        
  def parseR10_Parcelas(self):
    dicValuesR10_Parcelas = self.dicR10_Parcelas()
    self.parser.nextTag()
    while True:
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_RecintoSIGPAC":
        self.parseLD_RecintoSIGPAC()
      else:
        self.insertActualTag(dicValuesR10_Parcelas)
        if self.num_PA_NumOrden==0 and "PA_NumOrden" in dicValuesR10_Parcelas:
          self.num_PA_NumOrden = dicValuesR10_Parcelas["PA_NumOrden"]
          self.ID_PARCELA = "%s%05d" % (self.actual_RSU_NumExpediente,int(self.num_PA_NumOrden))
          dicValuesR10_Parcelas["ID_PARCELA"]=self.ID_PARCELA

      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("R10_Parcelas", "RSUPAC2019_R10_PARCELAS", dicValuesR10_Parcelas)
      if statusBlock == True: 
        self.num_PA_NumOrden = 0
        self.ID_PARCELA = 0
        break

  def dicLD_RecintoSIGPAC(self):
    dic = {"ID_RECINTO": self.num_LD_RecintoSIGPAC, "ID_PARCELA": self.ID_PARCELA}
    self.num_LD_RecintoSIGPAC+=1
    return dic

  def parseLD_RecintoSIGPAC(self):
    dicValues = self.dicLD_RecintoSIGPAC()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      if checkStart and parserTagName=="LD_Linea_AyudaSolAD":
        self.parseLD_Linea_AyudaSolAD()
      elif checkStart and parserTagName=="LD_Linea_AyudaSolPDR":
        self.parseLD_Linea_AyudaSolPDR()
      elif checkStart and parserTagName=="CultivoSecundario":
        self.parseCultivoSecundario(dicValues)
      elif checkStart and parserTagName=="CultivosHorticolas":
        self.parseCultivosHorticolas()
      elif checkStart and parserTagName=="R10Graf":
        self.parseR10Graf(dicValues)
      else:
        self.insertActualTag(dicValues)
      
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("LD_RecintoSIGPAC", "RSUPAC2019_RECINTOS_SIGPAC", dicValues)
      if statusBlock == True: break

  def parseR10Graf(self, dic):
    name = self.parser.getName()
    self.parser.nextTag()

    completo = None
    wkt = None
    srid= None
    
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="SRID":
      srid = self.parser.nextText()
      self.parser.nextTag()
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Completo":
      completo = self.parser.nextText()
      dic["Completo"] = completo
      self.parser.nextTag()
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="WKT":
      wkt = self.parser.nextText()
      self.parser.nextTag()
    if wkt != None:
      g = self.checkAndTransformWKT(wkt, srid)
      dic["GEOMETRY"] = g

  def dicAyudaSecundario(self):
    dic = {"ID": self.num_AyudaSecundario, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_AyudaSecundario+=1
    return dic
    
  def parseAyudaSecundario(self):
    dicValues = self.dicAyudaSecundario()
    self.parser.nextTag()
    while True:
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("AyudaSecundario", "RSUPAC2019_RECINTOS_SIGPAC_AS", dicValues)
      if statusBlock == True: break

  def dicCultivosHorticolas(self):
    dic = {"ID": self.num_CultivosHorticolas, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_CultivosHorticolas+=1
    return dic

  def parseCultivosHorticolas(self):
    dicValues = self.dicCultivosHorticolas()
    self.parser.nextTag()
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="CultivosHorticolas":
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("CultivosHorticolas", "RSUPAC2019_RECINTOS_SIGPAC_CH", dicValues)
      if statusBlock == True: break
      
  def parseCultivoSecundario(self, dicValues):
    self.parser.nextTag()
    while True:
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="AyudaSecundario":  # dentro de OtrosDatos
        self.parseAyudaSecundario()
      else:
        self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockCheck("CultivoSecundario")
      if statusBlock == True: break
        
  def dicLD_Linea_AyudaSolPDR(self):
    dic = {"ID": self.num_LD_Linea_AyudaSolPDR, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_LD_Linea_AyudaSolPDR+=1
    return dic

  def parseLD_Linea_AyudaSolPDR(self):
    dicValues = self.dicLD_Linea_AyudaSolPDR()
    self.parser.nextTag()
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_Linea_AyudaSolPDR":
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("LD_Linea_AyudaSolPDR", "RSUPAC2019_RECINTOS_SIGPAC_PDR", dicValues)
      if statusBlock == True: break
 
  def dicLD_Linea_AyudaSolAD(self):
    dic = {"ID": self.num_LD_Linea_AyudaSolAD, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_LD_Linea_AyudaSolAD+=1
    return dic

  def parseLD_Linea_AyudaSolAD(self):
    dicValues = self.dicLD_Linea_AyudaSolAD()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("LD_Linea_AyudaSolAD", "RSUPAC2019_RECINTOS_SIGPAC_AD", dicValues)
      if statusBlock == True: break

  def dicLinea_AyudaSolPDR(self):
    dic = {"ID": self.num_Linea_AyudaSolPDR, "NumExpediente":self.actual_RSU_NumExpediente}
    self.num_Linea_AyudaSolPDR+=1
    return dic
    
  def parseLinea_AyudaSolPDR(self):
    dicValues = self.dicLinea_AyudaSolPDR()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("Linea_AyudaSolPDR", "RSUPAC2019_AYUDA_SOL_PDR", dicValues)
      if statusBlock == True: break

  def endBlockCheck(self, nameTag):
    if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()==nameTag:
      return True
    return False
  def endBlockWithInsert(self, nameTag, nameTable, dicValues):
    if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()==nameTag:
      dicValues = fixFieldNames(dicValues)
      self.insertFactory.insert(nameTable, **dicValues)
      return True
    return False
    
  def dicLinea_AyudaSolAD(self):
    dic = {"ID": self.num_Linea_AyudaSolAD, "NumExpediente":self.actual_RSU_NumExpediente}
    self.num_Linea_AyudaSolAD+=1
    return dic
    
  def parseLinea_AyudaSolAD(self):
    dicValues = self.dicLinea_AyudaSolAD()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("Linea_AyudaSolAD", "RSUPAC2019_AYUDA_SOL_AD", dicValues)
      if statusBlock == True: break
        
  def dicExplotaciones(self):
    dic = {"ID": self.num_Explotaciones, "NumExpediente":self.actual_RSU_NumExpediente}
    self.num_Explotaciones+=1
    return dic
    
  def parseExplotaciones(self):
    dicValues = self.dicExplotaciones()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("Explotaciones", "RSUPAC2019_EXPLOTACIONES", dicValues)
      if statusBlock == True: break
        
  def dicLinea_OrigenAnimales(self):
    dic = {"ID": self.num_OrigenAnimales, "NumExpediente":self.actual_RSU_NumExpediente}
    self.num_OrigenAnimales+=1
    return dic
    
  def parseOrigenAnimales(self):
    dicValues = self.dicLinea_OrigenAnimales()
    self.parser.nextTag()
    while True:
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      self.insertActualTag(dicValues)
      self.parser.nextTag()
      statusBlock = self.endBlockWithInsert("OrigenAnimales", "RSUPAC2019_ORIGEN_ANIMALES", dicValues)
      if statusBlock == True: break
      

  def insertActualTag(self, dic):
    name = self.parser.getName()
    text = self.parser.nextText()
    dic[name] = text
    
  def read(self):
    self.next()

  def next(self):
    if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU":
      return None
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU":
      while self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU":
        if self.status!=None:
          self.status.incrementCurrentValue()
        self.parseRSU()
        self.parser.nextTag()
        
    if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU":
      return None
    return
    
  def parse(self, dbwriter, xmlfile): 
    # Recive un DBWriter y un File al XML y parsea el XML
    # llamando al writer para escribir los datos en la BBDD
    # Cada vez que lee un registo SRU debe llamar a self.status.incrementCurrentValue()

    # Esta implementacion es para poder probar el dbwriter.
    self.insertFactory = dbwriter
    self.fname = xmlfile
    self.open()
    self.read()

def changeFieldNameDictionary():
  d = { "Nombre_Conyuge": "Nombre_Conyuge_Solicitud",
  "Apellido1_Conyuge":"Apellido1_Conyuge_Solicitud",
  "Apellido2_Conyuge":"Apellido2_Conyuge_Solicitud",
  "Extran_Conyuge":"Extran_Conyuge_Solicitud",
  "ID_Conyuge":"ID_Conyuge_Solicitud",
  "RegMatrimonial_Conyuge":"RegMatrimonial_Conyuge_Solicitud",
  "Nombre_Repres":"Nombre_Repres_Solicitud",
  "Apellido1_Repres":"Apellido1_Repres_Solicitud",
  "Apellido2_Repres":"Apellido2_Repres_Solicitud",
  "Extran_Repres":"Extran_Repres_Solicitud",
  "ID_Repres":"ID_Repres_Solicitud",
  "SolGrupoEmpresarial":"SolGrupoEmpresarial_Solicitud",
  "Relacion_Con_Titular":"Relacion_Con_Titular_JE_Solicitud",
  "Comparte_resp_gestion":"Comparte_resp_gestion_JE_Solicitud",
  "Extran_JE":"Extran_JE_Solicitud",
  "ID_JE":"ID_JE_Solicitud",
  "Nombre_JE":"Nombre_JE_Solicitud",
  "Apellido1_JE":"Apellido1_JE_Solicitud",
  "Apellido2_JE":"Apellido2_JE_Solicitud",
  "Fnacimiento_JE":"Fnacimiento_JE_Solicitud",
  "Sexo_JE":"Sexo_JE_Solicitud",
  "Tfno_JE":"Tfno_JE_Solicitud",
  "TfnoMovil_JE":"TfnoMovil_JE_Solicitud",
  "email_JE":"email_JE_Solicitud",
  "PorcTA_JE":"PorcTA_JE_Solicitud",
  "AnoInicio_JE":"AnoInicio_JE_Solicitud",
  "FormAgraria_JE":"FormAgraria_JE_Solicitud",
  "CursosPerfe_JE":"CursosPerfe_JE_Solicitud",
  "IBAN":"IBAN_DB_Solicitud",
  "Banco":"Banco_DB_Solicitud",
  "Sucursal":"Sucursal_DB_Solicitud",
  "DC":"DC_DB_Solicitud",
  "CCC":"CCC_DB_Solicitud",
  "CodREGEPA":"CodREGEPA_OD_Solicitud",
  "VentaDirecta":"VentaDirecta_OD_Solicitud",
  "IA":"IA_OD_Solicitud",
  "PrimeraAA":"PrimeraAA_OD_Solicitud",
  "JovenGan":"JovenGan_OD_Solicitud",
  "NuevoGan":"NuevoGan_OD_Solicitud",
  "OPFH":"OPFH_OD_Solicitud",
  "CA_OPFH":"CA_OPFH_OD_Solicitud",
  "Razon_Social_OPFH":"Razon_Social_OPFH_OD_Solicitud",
  "OI_algodon":"OI_algodon_OD_Solicitud",
  "CIF_OI":"CIF_OI_OD_Solicitud",
  "NIF_CIF_integradora":"NIF_CIF_integradora_OD_Solicitud",
  "IA_integrado":"IA_integrado_OD_Solicitud",
  "Cebadero_comunitario":"Cebadero_comunitario_OD_Solicitud",
  "CIF_cebadero_comunitario":"CIF_cebadero_comunitario_OD_Solicitud",
  "SupDeclarada":"SupDeclarada_RS_Solicitud",
  "PP5anos":"PP5anos_RS_Solicitud",
  "Otras_supforrajeras":"Otras_supforrajeras_RS_Solicitud"
  }
  return d
  
def fixFieldNames(tofix):
  new = {}
  fixedFields = changeFieldNameDictionary()
  for k in tofix.keys():
    if k in fixedFields:
      new[fixedFields[k]]=tofix[k]
    else:
      new[k]=tofix[k]
  return new
  
def main():
  #t1 = {"Otras_supforrajeras": 1, "SupDeclarada": 2}
  #print changeFieldNameDictionary()
  #print fixFieldNames(t1)
  #return
  #from r10grafreader import test, selfRegister, R10GrafReaderFactory
  #selfRegister()
  fname = gvsig.getResource(__file__,"datos","test","RSU_PAC_2019_extra.xml")
  #fname = gvsig.getResource(__file__,"RSU_PAC_2019_muestra.xml")
  #test(R10GrafReaderFactory(), fname)
  # Uso del pull en java: DynclassImportHelper
  # importDefinitions
  from java.io import File
  xmlfile = File(fname)
  parser = RSUGrafParser()
  parser.parse(RSUInsertFeatures(), xmlfile)