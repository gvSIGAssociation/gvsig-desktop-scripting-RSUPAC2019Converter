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

class RSUInsertFeatures(object):
  def __init__(self):
    pass
  def insert(self, nombretabla, **params):
    #if nombretabla == "R10_Parcelas":
    print "@@@@@@@ INSERT IN ", nombretabla, " VALUES:", params
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
    ScriptingUtils.log(ScriptingUtils.WARN, "Loading file xml "+ self.fname)
    self.resource = FileInputStream(File(self.fname))
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
    self.num_PA_NumOrden = 0
  def checkAndTransformWKT(self, wkt, srid):
    geom = None
    if wkt!=None:
      if "EMPTY" in wkt:
        #ScriptingUtils.log(ScriptingUtils.WARN, "La geometria no es valida en %s:%s, el poligono esta vacio" % (self.num_expediente, self.num_parcela))
        pass
      else:
        geom = GeometryUtils.createFrom(wkt, srid)
        if geom!=None and not geom.isValid():
          #status = geom.getValidationStatus()
          #msg = status.getMessage()
          #ScriptingUtils.log(ScriptingUtils.WARN, "La geometria no es valida en %s:%s, %s" % (self.num_expediente, self.num_parcela, msg))
          geom = None
      
      if geom!=None and not isinstance(geom,MultiPolygon):
        geom = geom.toPolygons()
    return geom

  def dicR10_Parcelas(self):
    ID_PARCELA = "%20.20s%05d" % (self.num_RSU,float(self.num_PA_NumOrden))
    dic = {"ID_PARCELA": ID_PARCELA, "NumExpediente":self.num_RSU}
    self.num_R10_Parcelas+=1
    return dic
    
  def readRSU(self):
    ## Start with expediente
    self.parser.require(XmlPullParser.START_TAG, "", "RSU")
    dicRSU = {} ### VALORES DEL RSU
    unboundedR00_Solicitante = []
    self.parser.nextTag()
    self.insertActualTag(dicRSU)
    n = 0
    while True:
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()!="RSU":
        pass
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
        print "######## R10 PARCELAS"
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
            a,b = self.insertActualTag(dicValuesR10_Parcelas)
            if a=="PA_NumOrden":
              self.num_PA_NumOrden = b

          # Ending while setting new
          #print "last here: ", self.parser.getName(), "start:", self.parser.getEventType() == XmlPullParser.START_TAG , "end:", self.parser.getEventType() == XmlPullParser.END_TAG
          #print dicValuesR10_Parcelas
          if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="R10_Parcelas":
            self.insertFactory.insert("R10_Parcelas", **dicValuesR10_Parcelas)
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
        #print "tak1"
        if self.parser.getName()=="NumExpediente":
          self.num_RSU = self.parser.nextText()

        if self.parser.getEventType() != XmlPullParser.END_TAG:
          #print "tak2", self.parser.getEventType()==XmlPullParser.START_TAG, self.parser.getName()
          self.insertActualTag(dicRSU)
      
      
      if n>5000:
        print "#2 out of 5000"
        break
      else:
        n+=1

      # end of document
      try:
        self.parser.nextTag()
      except:
        break
      # if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="RSU":
      # todo: deberia de ponerse algo similar para cuando hayan tags que no se analizan
      if self.parser.getEventType() == XmlPullParser.END_TAG and self.parser.getName()=="RSU":
        break
    print "Insert RSU"
    self.insertFactory.insert("RSU", **dicRSU)
    print "# END RSU"
  def dicLD_RecintoSIGPAC(self):
    dic = {"ID_RECINTO": self.num_LD_RecintoSIGPAC, "ID_PARCELA":self.num_R10_Parcelas}
    self.num_LD_RecintoSIGPAC+=1
    return dic
  def insertLD_RecintoSIGPAC(self):
    print "######## R10 PARCELAS - insertLD_RecintoSIGPAC"
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
        self.insertFactory.insert("LD_RecintoSIGPAC", **dicValues)
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
    print "* r10graf: insertLinea_R10Graf"
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
      #self.parser.nextTag()
      print wkt
    if wkt != None:
      g = self.checkAndTransformWKT(wkt, srid)
      #TODO: g.setProjection()
      dic["GEOMETRY"] = g
      print "GEOMETRY:", g
    #self.parser.nextTag()
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
        self.insertFactory.insert("AyudaSecundario", **dicValues)
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
      #elif checkStart and parserTagName=="unbounded":
      #  unbounded = {}
      #  self.insertLinea_unbounded(unbounded)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="CultivosHorticolas": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="CultivosHorticolas": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("CultivosHorticolas", **dicValues)
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
    print "######## R10 PARCELAS/LD_RecintoSIGPAC - insertLD_Linea_AyudaSolPDR ****************"
    n = 0
    dicValues = self.dicLD_Linea_AyudaSolPDR()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_Linea_AyudaSolPDR":
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
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="LD_Linea_AyudaSolPDR": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolPDR": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("LD_Linea_AyudaSolPDR", **dicValues)
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
    print "######## R10 PARCELAS/LD_RecintoSIGPAC - insertLD_Linea_AyudaSolAD ****************"
    n = 0
    dicValues = self.dicLD_Linea_AyudaSolAD()
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="LD_Linea_AyudaSolAD":
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
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="LD_Linea_AyudaSolAD": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolAD": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("LD_Linea_AyudaSolAD", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="LD_Linea_AyudaSolAD": # Si hay otro del unbounded
          dicValues = self.dicLD_Linea_AyudaSolAD()
          self.parser.nextTag()
        else:
          break # Si no es otro cambia de bloque
      if n>5000:
        break
      else:
        n+=1
  def dicLinea_AyudaSolAD(self):
    dic = {"ID": self.num_Linea_AyudaSolAD, "NumExpediente":self.num_RSU}
    self.num_Linea_AyudaSolAD+=1
    return dic
  def insertLinea_AyudaSolAD(self):
    print "######## R00 SOLICITUD/ResumenSol - insertLinea_AyudaSolAD ****************"
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
      #elif checkStart and parserTagName=="unbounded":
      #  unbounded = {}
      #  self.insertLinea_unbounded(unbounded)

      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="Linea_AyudaSolAD": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Linea_AyudaSolAD": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("Linea_AyudaSolAD", **dicValues)
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
    print "######## R00 SOLICITUD/OTROS DATOS - insertExplotaciones"
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
      #elif checkStart and parserTagName=="unbounded":
      #  unbounded = {}
      #  self.insertLinea_unbounded(unbounded)
      
      # Ending while setting new
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()!="Explotaciones": # Cuando siguen tags despues de unbounded
        pass
      else:
        self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="Explotaciones": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("Explotaciones", **dicValues)
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
    self.parser.nextTag() # pasa el <R10_Parcelas>
    while self.parser.getEventType() != XmlPullParser.END_TAG and self.parser.getName()!="OrigenAnimales":
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
      self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="OrigenAnimales": # Si hay otro del unbounded
          self.parser.nextTag()
      if self.parser.getEventType() == XmlPullParser.END_TAG: # and self.parser.getName()!="R10_Parcelas": # Si se llega al tag final del bloque unbounded
        self.parser.nextTag()
        self.insertFactory.insert("OrigenAnimales", **dicValues)
        if self.parser.getEventType() == XmlPullParser.START_TAG and self.parser.getName()=="OrigenAnimales": # Si hay otro del unbounded
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
    self.xml = xmlfile
    
    self.read()
      
def main():
  #from r10grafreader import test, selfRegister, R10GrafReaderFactory
  #selfRegister()
  fname = gvsig.getResource(__file__,"RSU_PAC_2019_muestra.xml")
  #fname = gvsig.getResource(__file__,"RSU_PAC_2019_muestra.xml")
  #test(R10GrafReaderFactory(), fname)
  # Uso del pull en java: DynclassImportHelper
  # importDefinitions
  parser = RSUGrafParser(fname)
  parser.open()
  
  print "Values:", parser.read()