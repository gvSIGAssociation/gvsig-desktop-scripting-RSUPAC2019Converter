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

class RSUInsertFeatures(object):
  def __init__(self):
    self.m = 0
    pass
    
    
  def insert(self, nombretabla, **params):
    
    if nombretabla == "RSUPAC2019_RECINTOS_SIGPAC_AD":
      import pprint
      pp = pprint.PrettyPrinter(indent=4)
      print self.m, "@@@@@@@ INSERT IN ", nombretabla, " VALUES:",
      self.m +=1
      pp.pprint(params)

      #print "@@@@@@@ INSERT IN ", nombretabla, " VALUES:", params
    pass
    
class RSUGrafParser(object):
  
  def __init__(self, status, fname=None):
    self.status = status
    self.insertFactory = RSUInsertFeatures()
    self.fname = fname
    self.xml = None
    factory = XmlPullParserFactory.newInstance(ToolsLocator.getInstance().getXmlPullParserFactoryClassNames(),None)
    self.parser = factory.newPullParser()
    self.initValues()
    self.dbwriter = None
    self.count = 0

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
    print "# end open"

  def readInitValues(self):
    self.parser.nextTag()
    self.parser.require(XmlPullParser.START_TAG, None, "Expedientes_RSU")
    self.parser.nextTag()

  def initValues(self):
    # Reset and init values
    self.done = False
    self.num_RSU = 0
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
    dic = {"ID_PARCELA": 999, "NumExpediente":self.num_RSU}
    self.num_R10_Parcelas+=1
    return dic
    
  def readRSU(self):
    ## Start with expediente
    self.parser.require(XmlPullParser.START_TAG, "", "RSU")
    dicRSU = {} ### VALORES DEL RSU
    self.parser.nextTag()
    self.insertActualTag(dicRSU)
    n = 0
    
    while True:
      #if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()!="RSU":
      #  print "end rsu"
      #  pass
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU": # Cuando siguen tags despues de unbounded
        break
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R00_Solicitante":
        self.parser.nextTag() # pasa el <R00_Solicitante>
        while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="R00_Solicitante":
          self.insertActualTag(dicRSU)
          self.parser.nextTag()
          if n>5000:
            print "#3 out of 5000"
            break
          else:
            n+=1
        # rellena el RSU
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R00_Solicitud":
        self.parser.nextTag() # pasa el <R00_Solicitud>
        while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="R00_Solicitud":
          checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
          parserTagName = self.parser.getName()
          
          if self.parser.getEventType() == XmlPullParser.END_TAG:
            pass
          elif checkStart and parserTagName=="Conyuge":
            pass
          elif checkStart and parserTagName=="Representante":
            pass
          elif checkStart and parserTagName=="RespJuridica":
            pass
          elif checkStart and parserTagName=="JefeExplotacion":
            pass
          elif checkStart and parserTagName=="DatosBancarios":
            pass
          elif checkStart and parserTagName=="OtrosDatos":
            pass          
          elif checkStart and parserTagName=="Explotaciones":  # dentro de OtrosDatos
            self.insertExplotaciones()
          elif checkStart and parserTagName=="OrigenAnimales":  # dentro de OtrosDatos
            self.insertLinea_OrigenAnimales()
          elif checkStart and self.parser.getName()=="JefeExplotacion":
            pass
          elif checkStart and self.parser.getName()=="ResumenSol":
            pass
          elif checkStart and parserTagName=="Linea_AyudaSolAD":  # dentro de ResumenSol
            self.insertLinea_AyudaSolAD()
          else:
            self.insertActualTag(dicRSU)
          #print "nexttag: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG

          self.parser.nextTag()
          if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()!="R00_Solicitud":
            self.parser.nextTag()
          if n>5000:
            print "while safety: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
            break
          else:
            n+=1
        #rellena el RSU #not valid -> self.insertFactory.insert("R00_Solicitud", dicR00_Solicitud)
        
      elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R10_Parcelas":
        #print "######## R10 PARCELAS"
        dicValuesR10_Parcelas = self.dicR10_Parcelas()
        #print "R10 Init Parcelas. start:", self.parser.getEventType() == XmlPullParser.START_TAG, " end: ",self.parser.getEventType() == XmlPullParser.END_TAG, "name: ", self.parser.getName()
        self.parser.nextTag() # pasa el <R10_Parcelas>
        while True:
          #print "R10 Parcelas. start:", self.parser.getEventType() == XmlPullParser.START_TAG, " end: ",self.parser.getEventType() == XmlPullParser.END_TAG, "name: ", self.parser.getName()
          if self.parser.getEventType() == XmlPullParser.END_TAG:
            pass
          elif self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_RecintoSIGPAC":
            self.insertLD_RecintoSIGPAC()
          else:
            self.insertActualTag(dicValuesR10_Parcelas)
            if "PA_NumOrden" in dicValuesR10_Parcelas:
              self.num_PA_NumOrden = dicValuesR10_Parcelas["PA_NumOrden"]
              self.ID_PARCELA = "%s%05d" % (self.num_RSU,int(self.num_PA_NumOrden))
              dicValuesR10_Parcelas["ID_PARCELA"]=self.ID_PARCELA

          # Ending while setting new
          #print "last here: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
          #print dicValuesR10_Parcelas
          if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="R10_Parcelas":
            dicValuesR10_Parcelas = fixFieldNames(dicValuesR10_Parcelas)
            self.insertFactory.insert("RSUPAC2019_R10_PARCELAS", **dicValuesR10_Parcelas)
            dicValuesR10_Parcelas = self.dicR10_Parcelas()
          if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="R10_Parcelas": # Cuando siguen tags despues de unbounded
            pass
          else:
            self.parser.nextTag()
          if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R10_Parcelas": # Si hay otro del unbounded
              self.parser.nextTag()
          if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
            #self.insertFactory.insert("R10_Parcelas", dicValuesR10_Parcelas)
            self.parser.nextTag()
            if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="R10_Parcelas": # Si hay otro del unbounded
              self.parser.nextTag()
            else:
              break # Si no es otro cambia de bloque
          if n>5000:
            break
          else:
            n+=1
      else:
        #print "last here: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
        if self.parser.getEventType() != XmlPullParser.END_TAG:
          self.insertActualTag(dicRSU)
        if "NumExpediente" in dicRSU:
          self.num_RSU = dicRSU["NumExpediente"]
      if n>5000:
        print "#2 out of 5000"
        break
      else:
        n+=1

      # Ending while setting new
      #print "last here: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
      #print self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="RSU"
      #print dicValues
      
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU":
        dicRSU = fixFieldNames(dicRSU)
        self.insertFactory.insert("RSUPAC2019_EXPEDIENTES", **dicRSU)
        self.status.incrementCurrentValue()
        dicValuesR10_Parcelas = self.dicR10_Parcelas()
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU": # Cuando siguen tags despues de unbounded
        dicRSU = fixFieldNames(dicRSU)
        self.insertFactory.insert("RSUPAC2019_EXPEDIENTES", **dicRSU)
        self.status.incrementCurrentValue()
        break
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="RSU": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU": # Si hay otro del unbounded
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        #dicRSU = fixFieldNames(dicRSU)
        #self.insertFactory.insert("RSUPAC2019_EXPEDIENTES", **dicRSU)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU": # Si hay otro del unbounded
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
       
  def dicLD_RecintoSIGPAC(self): #num_PA_NumOrden
    dic = {"ID_RECINTO": self.num_LD_RecintoSIGPAC, "ID_PARCELA": self.ID_PARCELA}
    self.num_LD_RecintoSIGPAC+=1
    return dic
  def insertLD_RecintoSIGPAC(self):
    #print "######## R10 PARCELAS - insertLD_RecintoSIGPAC"
    n = 0
    dicValues = self.dicLD_RecintoSIGPAC()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_RecintoSIGPAC":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      elif checkStart and parserTagName=="LD_Linea_AyudaSolAD":
        self.insertLD_Linea_AyudaSolAD()
      elif checkStart and parserTagName=="LD_Linea_AyudaSolPDR":
        self.insertLD_Linea_AyudaSolPDR()
      elif checkStart and parserTagName=="CultivoSecundario":
        pass #not unbounded
      elif checkStart and parserTagName=="AyudaSecundario":
        self.insertAyudaSecundario()
      elif checkStart and parserTagName=="CultivosHorticolas":
        self.insertCultivosHorticolas()
      elif checkStart and parserTagName=="R10Graf":
        # Trato coon funcion aparte porque tengo que crear la geometria
        self.insertLinea_R10Graf(dicValues)
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      #print "last here: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
      #print dicValues
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="LD_RecintoSIGPAC": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_RecintoSIGPAC": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_RECINTOS_SIGPAC", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_RecintoSIGPAC": # Si hay otro del unbounded
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1

  def insertLinea_R10Graf(self, dic):
    # No es unbounded.
    #print "* r10graf: insertLinea_R10Graf"
    name = self.parser.getName()
    self.parser.nextTag()

    completo = None
    wkt = None
    srid= None
    
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="SRID":
      srid = self.parser.nextText()
      self.parser.nextTag()
      #self.parser.nextTag()
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Completo":
      completo = self.parser.nextText()
      dic["Completo"] = completo
      self.parser.nextTag()
      #self.parser.nextTag()
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="WKT":
      wkt = self.parser.nextText()
      self.parser.nextTag()
    if wkt != None:
      g = self.checkAndTransformWKT(wkt, srid)
      dic["GEOMETRY"] = g
      print "GEOMETRY:", g
    
  def dicAyudaSecundario(self):
    dic = {"ID": self.num_AyudaSecundario, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_AyudaSecundario+=1
    return dic
  def insertAyudaSecundario(self):
    print "######## R10 PARCELAS/LD_RecintoSIGPAC - insertAyudaSecundario"
    n = 0
    dicValues = self.dicAyudaSecundario()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="AyudaSecundario":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)
      #elif checkStart and parserTagName=="unbounded":
      #  unbounded = {}
      #  self.insertLinea_unbounded(unbounded)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="AyudaSecundario": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="AyudaSecundario": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_RECINTOS_SIGPAC_AS", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="AyudaSecundario": # Si hay otro del unbounded
          dicValues = self.dicAyudaSecundario()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1

  def dicCultivosHorticolas(self):
    dic = {"ID": self.num_CultivosHorticolas, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_CultivosHorticolas+=1
    return dic

  def insertCultivosHorticolas(self):
    print "######## R10 PARCELAS/LD_RecintoSIGPAC - insertCultivosHorticolas"
    n = 0
    dicValues = self.dicCultivosHorticolas()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="CultivosHorticolas":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="CultivosHorticolas": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="CultivosHorticolas": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_RECINTOS_SIGPAC_CH", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="CultivosHorticolas": # Si hay otro del unbounded
          dicValues = self.dicCultivosHorticolas()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
  def dicLD_Linea_AyudaSolPDR(self):
    dic = {"ID": self.num_LD_Linea_AyudaSolPDR, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_LD_Linea_AyudaSolPDR+=1
    return dic

  def insertLD_Linea_AyudaSolPDR(self):
    #print "######## R10 PARCELAS/LD_RecintoSIGPAC - insertLD_Linea_AyudaSolPDR"
    n = 0
    dicValues = self.dicLD_Linea_AyudaSolPDR()
    self.parser.nextTag()
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_Linea_AyudaSolPDR":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="LD_Linea_AyudaSolPDR": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolPDR": # Si hay otro del unbounded
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_RECINTOS_SIGPAC_PDR", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolPDR": # Si hay otro del unbounded
          dicValues = self.dicLD_Linea_AyudaSolPDR()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
  def dicLD_Linea_AyudaSolAD(self):
    dic = {"ID": self.num_LD_Linea_AyudaSolAD, "ID_RECINTO":self.num_LD_RecintoSIGPAC}
    self.num_LD_Linea_AyudaSolAD+=1
    return dic
  def insertLD_Linea_AyudaSolAD(self):
    #print "######## R10 PARCELAS/LD_RecintoSIGPAC - LD_Linea_AyudaSolAD"
    n = 0
    dicValues = self.dicLD_Linea_AyudaSolAD()
    self.parser.nextTag()
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_Linea_AyudaSolAD":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="LD_Linea_AyudaSolAD": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolAD": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_RECINTOS_SIGPAC_AD", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolAD": # Si hay otro del unbounded
          dicValues = self.dicLD_Linea_AyudaSolAD()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
      pass
        
  def dicLinea_AyudaSolAD(self):
    dic = {"ID": self.num_Linea_AyudaSolAD, "NumExpediente":self.num_RSU}
    self.num_Linea_AyudaSolAD+=1
    return dic
    
  def insertLinea_AyudaSolAD(self):
    #print "######## R00 SOLICITUD/ResumenSol - Linea_AyudaSolAD"
    n = 0
    dicValues = self.dicLinea_AyudaSolAD()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="Linea_AyudaSolAD":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="Linea_AyudaSolAD": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Linea_AyudaSolAD": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_AYUDA_SOL_AD", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Linea_AyudaSolAD": # Si hay otro del unbounded
          dicValues = self.dicLinea_AyudaSolAD()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
  def dicExplotaciones(self):
    dic = {"ID": self.num_Explotaciones, "NumExpediente":self.num_RSU}
    self.num_Explotaciones+=1
    return dic
    
  def insertExplotaciones(self):
    #print "######## R00 SOLICITUD/OTROS DATOS - insertExplotaciones"
    n = 0
    dicValues = self.dicExplotaciones()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="Explotaciones":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="Explotaciones": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Explotaciones": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_EXPLOTACIONES", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Explotaciones": # Si hay otro del unbounded
          dicValues = self.dicExplotaciones()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
  def dicLinea_OrigenAnimales(self):
    dic = {"ID": self.num_Linea_OrigenAnimales, "NumExpediente":self.num_RSU}
    self.num_Linea_OrigenAnimales+=1
    return dic
  def insertLinea_OrigenAnimales(self):
    print "######## R00 SOLICITUD/OTROS DATOS - insertLinea_OrigenAnimales"
    n = 0
    dicValues = self.dicLinea_OrigenAnimales()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="OrigenAnimales":
      checkStart = self.parser.getEventType() == XmlPullParser.START_TAG
      parserTagName = self.parser.getName()
      
      if self.parser.getEventType() == XmlPullParser.END_TAG:
        pass
      else:
        self.insertActualTag(dicValues)

      # Ending while setting new
      self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="OrigenAnimales": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        dicValues = fixFieldNames(dicValues)
        self.insertFactory.insert("RSUPAC2019_ORIGEN_ANIMALES", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="OrigenAnimales": # Si hay otro del unbounded
          dicValues = self.dicLinea_OrigenAnimales()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1

  def insertActualTag(self, dic):
    name = self.parser.getName()
    #print "insertActualtag:", name,
    text = self.parser.nextText()
    #print  text
    dic[name] = text
    return name, text
    
  def read(self):
    if self.isDone():
      return None
    self.next()

  def next(self):
    if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="Expedientes_RSU":
        self.done = True
        return None
    if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="RSU":
      self.readRSU()
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
  fname = gvsig.getResource(__file__,"datos","test","RSU_PAC_2019_muestra.xml")
  #fname = gvsig.getResource(__file__,"RSU_PAC_2019_muestra.xml")
  #test(R10GrafReaderFactory(), fname)
  # Uso del pull en java: DynclassImportHelper
  # importDefinitions
  from java.io import File
  xmlfile = File(fname)
  parser = RSUGrafParser(fname)
  parser.parse(RSUInsertFeatures(), xmlfile)
  
  print "Values:", parser.read()