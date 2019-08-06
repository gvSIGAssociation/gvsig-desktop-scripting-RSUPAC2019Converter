# encoding: utf-8

import gvsig

from gvsig import getResource

from java.io import File, FileInputStream

from org.xmlpull.v1 import XmlPullParser
from org.xmlpull.v1.XmlPullParser  import START_TAG, END_TAG
from org.xmlpull.v1 import XmlPullParserException
from org.xmlpull.v1 import XmlPullParserFactory

from org.gvsig.tools import ToolsLocator
from org.gvsig.fmap.geom import GeometryUtils
from org.gvsig.fmap.crs import CRSFactory

from addons.RSUPAC2019Importer.parsers.rsuparser import RSUParser
from addons.RSUPAC2019Importer.trace import trace, trace_remove

def create_parser(status):
  return XmlParser2(status)


class Counters(object):
  def __init__(self, **counters):
    self.counters = counters

  def get(self, name):
    v = self.counters.get(name,0)
    self.counters[name] = v+1
    return v

COUNTERS = Counters()

class Expediente(object):
  def __init__(self):
    self.Ano = None
    self.CA_Expediente = None
    self.ProvExpediente = None
    self.CRExpediente = None
    self.NumExpediente = None
    self.Fregistro = None
    self.Fmodificacion = None
    self.ID_Solicitante = None
    self.Nombre_Solicitante = None
    self.Apellido1_Solicitante = None
    self.Apellido2_Solicitante = None
    self.Fnacimiento_Solicitante = None
    self.Sexo_Solicitante = None
    self.Direccion_Solicitante = None
    self.Localidad_Solicitante = None
    self.CodMunicipio_Solicitante = None
    self.CodPostal_Solicitante = None
    self.Tfno_Solicitante = None
    self.TfnoMovil_Solicitante = None
    self.email_Solicitante = None
    self.Tipo_EJ_Solicitante = None
    self.TitComp_Solicitante = None
    self.Nombre_Conyuge_Solicitud = None
    self.Apellido1_Conyuge_Solicitud = None
    self.Apellido2_Conyuge_Solicitud = None
    self.Extran_Conyuge_Solicitud = None
    self.ID_Conyuge_Solicitud = None
    self.RegMatrimonial_Conyuge_Solicitud = None
    self.Nombre_Repres_Solicitud = None
    self.Apellido1_Repres_Solicitud = None
    self.Apellido2_Repres_Solicitud = None
    self.Extran_Repres_Solicitud = None
    self.ID_Repres_Solicitud = None
    self.SolGrupoEmpresarial_Solicitud = None
    self.Relacion_Con_Titular_JE_Solicitud = None
    self.Comparte_resp_gestion_JE_Solicitud = None
    self.Extran_JE_Solicitud = None
    self.ID_JE_Solicitud = None
    self.Nombre_JE_Solicitud = None
    self.Apellido1_JE_Solicitud = None
    self.Apellido2_JE_Solicitud = None
    self.Fnacimiento_JE_Solicitud = None
    self.Sexo_JE_Solicitud = None
    self.Tfno_JE_Solicitud = None
    self.TfnoMovil_JE_Solicitud = None
    self.email_JE_Solicitud = None
    self.PorcTA_JE_Solicitud = None
    self.AnoInicio_JE_Solicitud = None
    self.FormAgraria_JE_Solicitud = None
    self.CursosPerfe_JE_Solicitud = None
    self.IBAN_DB_Solicitud = None
    self.Banco_DB_Solicitud = None
    self.Sucursal_DB_Solicitud = None
    self.DC_DB_Solicitud = None
    self.CCC_DB_Solicitud = None
    self.CodREGEPA_OD_Solicitud = None
    self.VentaDirecta_OD_Solicitud = None
    self.IA_OD_Solicitud = None
    self.PrimeraAA_OD_Solicitud = None
    self.JovenGan_OD_Solicitud = None
    self.NuevoGan_OD_Solicitud = None
    self.OPFH_OD_Solicitud = None
    self.CA_OPFH_OD_Solicitud = None
    self.Razon_Social_OPFH_OD_Solicitud = None
    self.OI_algodon_OD_Solicitud = None
    self.CIF_OI_OD_Solicitud = None
    self.NIF_CIF_integradora_OD_Solicitud = None
    self.IA_integrado_OD_Solicitud = None
    self.Cebadero_comunitario_OD_Solicitud = None
    self.CIF_cebadero_comunitario_OD_Solicitud = None
    self.SupDeclarada_RS_Solicitud = None
    self.PP5anos_RS_Solicitud = None
    self.Otras_supforrajeras_RS_Solicitud = None    
    
    self.Explotaciones_OD_Solicitud = list()
    self.OrigenAnimales_OD_Solicitud = list()
    self.Linea_AyudaSolAD_RS_Solicitud = list()
    self.Linea_AyudaSolPDR_RS_Solicitud = list()
    self.R10_Parcelas = list()
    
    self.R11_Socios = list()
    self.R12_Entidades = list()
    self.R30_AnimalesPDR = list()
    self.R40_ApiculturaPDR = list()
    self.R50_EntidadesAsoc = None

  def write(self, writer):
    d = dict()
    for k,v in self.__dict__.iteritems():
      if k in ("Explotaciones_OD_Solicitud",
        "OrigenAnimales_OD_Solicitud",
        "Linea_AyudaSolAD_RS_Solicitud",
        "Linea_AyudaSolPDR_RS_Solicitud",
        "R10_Parcelas",
        "R11_Socios",
        "R12_Entidades",
        "R30_AnimalesPDR",
        "R40_ApiculturaPDR",
        "R50_EntidadesAsoc"):
        continue
      d[k] = v
    writer.insert("RSUPAC2019_EXPEDIENTES", **d)
    for x in self.Explotaciones_OD_Solicitud:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.OrigenAnimales_OD_Solicitud:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.Linea_AyudaSolAD_RS_Solicitud:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.Linea_AyudaSolPDR_RS_Solicitud:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.R10_Parcelas:
      x.NumExpediente = self.NumExpediente
      x.write(writer)

    for x in self.R11_Socios:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.R12_Entidades:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.R30_AnimalesPDR:
      x.NumExpediente = self.NumExpediente
      x.write(writer)
    for x in self.R40_ApiculturaPDR:
      x.NumExpediente = self.NumExpediente
      x.write(writer)


class Explotacion(object):
  def __init__(self):
    self.ID = None
    self.NumExpediente = None
    self.CodREGA = None

  def write(self, writer):
    self.ID = COUNTERS.get("Explotacione")
    writer.insert(
      "RSUPAC2019_EXPLOTACIONES", 
      ID=self.ID, 
      NumExpediente=self.NumExpediente, 
      CodREGA=self.CodREGA
    )

class OrigenAnimales(object):
  def __init__(self):
    self.ID = None
    self.NumExpediente = None
    self.CodREGA = None

  def write(self, writer):
    self.ID = COUNTERS.get("OrigenAnimales")
    writer.insert(
      "RSUPAC2019_ORIGEN_ANIMALES", 
      ID=self.ID, 
      NumExpediente=self.NumExpediente, 
      CodREGA=self.CodREGA
    )

class AyudaSolAD(object):
  def __init__(self):
    self.ID = None
    self.NumExpediente = None
    self.Codigo_lineaAD = None
    self.SupDeclarada_LineaAD = None

  def write(self, writer):
    self.ID = COUNTERS.get("AyudaSolAD")
    writer.insert(
      "RSUPAC2019_AYUDA_SOL_AD", 
      ID=self.ID, 
      NumExpediente=self.NumExpediente, 
      Codigo_lineaAD=self.Codigo_lineaAD,
      SupDeclarada_LineaAD=self.SupDeclarada_LineaAD
    )

class AyudaSolPDR(object):
  def __init__(self):
    self.ID = None
    self.NumExpediente = None
    self.Codigo_lineaPDR = None

  def write(self, writer):
    self.ID = COUNTERS.get("AyudaSolPDR")
    writer.insert(
      "RSUPAC2019_AYUDA_SOL_PDR", 
      ID=self.ID, 
      NumExpediente=self.NumExpediente, 
      Codigo_lineaPDR=self.Codigo_lineaPDR
    )

class R10Parcela(object):
  def __init__(self):
    self.ID_PARCELA = None
    self.NumExpediente = None

  def write(self, writer):
    d = dict()
    self.ID = COUNTERS.get("R10Parcelas")
    writer.insert("RSUPAC2019_R10_PARCELAS", **d)


class XmlParser2(RSUParser):
  def __init__(self, status):
    RSUParser.__init__(self, status)
    self.writer = None
    self.parser = None
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
  
  def parse(self, dbwriter, xmlfile): 
    # Recive un DBWriter y un File al XML y parsea el XML
    # llamando al writer para escribir los datos en la BBDD
    # Cada vez que lee un registo SRU debe llamar a self.status.incrementCurrentValue()

    self.writer = dbwriter
    self.xmlfile = xmlfile
    self.xmlis = FileInputStream(self.xmlfile);
    factory = XmlPullParserFactory.newInstance(
      ToolsLocator.getInstance().getXmlPullParserFactoryClassNames(),
      None
    )
    self.parser = factory.newPullParser()
    self.parser.setInput(self.xmlis, None)
    
    self.parser.nextTag()
    self.parser.require(START_TAG, None, "Expedientes_RSU")
    self.parser.nextTag()
    if self.parser.getEventType()==START_TAG and self.parser.getName() == "RSU":
      self.parse_SRU()
    self.parser.require(END_TAG, None, "Expedientes_RSU")

  def parse_SRU(self):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "RSU":
      expediente = Expediente()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "RSU"):
        if parser.getEventType()!=START_TAG:
          raise Exception("Error parsing xml. Expected a start tag in line %d" % parser.getLineNumber())
        name = parser.getName()
        if name == "Ano":
          expediente.Ano = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "CA_Expediente":
          expediente.CA_Expediente = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "ProvExpediente":
          expediente.ProvExpediente = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "CRExpediente":
          expediente.CRExpediente = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "NumExpediente":
          expediente.NumExpediente = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "Fregistro":
          expediente.Fregistro = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "Fmodificacion":
          expediente.Fmodificacion = parser.nextText()
          parser.require(END_TAG, None, name)
          parser.nextTag()
        elif name == "R00_Solicitante":
          self.parse_R00_Solicitante(expediente)
        elif name == "R00_Solicitud":
          self.parse_R00_Solicitud(expediente)
        elif name == "R10_Parcelas":
          self.parse_R10_Parcelas(expediente)
        elif name == "R11_Socios":
          self.parse_R11_Socios(expediente)
        elif name == "R12_Entidades":
          self.parse_R12_Entidades(expediente)
        elif name == "R30_AnimalesPDR":
          self.parse_R30_AnimalesPDR(expediente)
        elif name == "R40_ApiculturaPDR":
          self.parse_R40_ApiculturaPDR(expediente)
        elif name == "R50_EntidadesAsoc":
          self.parse_R50_EntidadesAsoc(expediente)
        else:
          raise Exception("Error parsing xml. Unexpected tag %r in line %d" % (name,parser.getLineNumber()))
  
      parser.require(END_TAG, None, "RSU")
      parser.nextTag()
      
      expediente.write(self.writer)
    
  def parse_R00_Solicitante(self, expediente):
    parser = self.parser
    parser.require(START_TAG, None, "R00_Solicitante")
    parser.nextTag()
    while not (parser.getEventType()==END_TAG and parser.getName() == "R00_Solicitante"):
      if parser.getEventType()!=START_TAG:
        raise Exception("Error parsing xml. Expected a start tag in line %d" % parser.getLineNumber())
      name = parser.getName()
      if name == "ID_Solicitante":
        expediente.ID_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Nombre_Solicitante":
        expediente.Nombre_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Apellido1_Solicitante":
        expediente.Apellido1_Solicitante= parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Apellido2_Solicitante":
        expediente.Apellido2_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Fnacimiento_Solicitante":
        expediente.Fnacimiento_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Sexo_Solicitante":
        expediente.Sexo_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Direccion_Solicitante":
        expediente.Direccion_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Localidad_Solicitante":
        expediente.Localidad_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "CodMunicipio_Solicitante":
        expediente.CodMunicipio_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "CodPostal_Solicitante":
        expediente.CodPostal_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Tfno_Solicitante":
        expediente.Tfno_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "TfnoMovil_Solicitante":
        expediente.TfnoMovil_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "email_Solicitante":
        expediente.email_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "Tipo_EJ_Solicitante":
        expediente.Tipo_EJ_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      elif name == "TitComp_Solicitante":
        expediente.TitComp_Solicitante = parser.nextText()
        parser.require(END_TAG, None, name)
        parser.nextTag()
      else:
        raise Exception("Error parsing xml. Unexpected tag %r in line %d" % (name,parser.getLineNumber()))

    parser.require(END_TAG, None, "R00_Solicitante")
    parser.nextTag()
    
  def parse_R00_Solicitud(self, expediente):
    parser = self.parser
    parser.require(START_TAG, None, "R00_Solicitud")
    parser.nextTag()
    while not (parser.getEventType()==END_TAG and parser.getName() == "R00_Solicitud"):
      parser.next()
    parser.require(END_TAG, None, "R00_Solicitud")
    parser.nextTag()

  def parse_R10_Parcelas(self, expediente):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "R10_Parcelas":
      parcela = R10Parcela()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "R10_Parcelas"):
        parser.next()
      parser.require(END_TAG, None, "R10_Parcelas")
      parser.nextTag()
      expediente.R10_Parcelas.append(parcela)

  def parse_R11_Socios(self, expediente):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "R11_Socios":
      #socio = R11Socio()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "R11_Socios"):
        parser.next()
      parser.require(END_TAG, None, "R11_Socios")
      parser.nextTag()
      #expediente.R11_Socios.append(socio)

  def parse_R12_Entidades(self, expediente):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "R12_Entidades":
      #entidad = R12Entidad()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "R12_Entidades"):
        parser.next()
      parser.require(END_TAG, None, "R12_Entidades")
      parser.nextTag()
      #expediente.R12_Entidades.append(entidad)

  def parse_R30_AnimalesPDR(self, expediente):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "R30_AnimalesPDR":
      #animal = R30AnimalePDR()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "R30_AnimalesPDR"):
        parser.next()
      parser.require(END_TAG, None, "R30_AnimalesPDR")
      parser.nextTag()
      #expediente.R30_AnimalesPDR.append(animal)

  def parse_R40_ApiculturaPDR(self, expediente):
    parser = self.parser
    while parser.getEventType()==START_TAG and parser.getName() == "R40_ApiculturaPDR":
      #apicultura = R40Apicultura()
      parser.nextTag()
      while not (parser.getEventType()==END_TAG and parser.getName() == "R40_ApiculturaPDR"):
        parser.next()
      parser.require(END_TAG, None, "R40_ApiculturaPDR")
      parser.nextTag()
      #expediente.R40_ApiculturaPDR.append(apicultura)

  def parse_R50_EntidadesAsoc(self, expediente):
    parser = self.parser
    parser.require(START_TAG, None, "R50_EntidadesAsoc")
    parser.nextTag()
    while parser.getEventType()!=END_TAG and parser.getName() == "R50_EntidadesAsoc":
        parser.next()
    parser.require(END_TAG, None, "R50_EntidadesAsoc")
    parser.nextTag()


def test():
  import os
  from java.io import File

  #from addons.RSUPAC2019Importer.parsers.xmlparser0 import create_parser
  #from addons.RSUPAC2019Importer.parsers.xmlparserfacade import create_parser

  #from addons.RSUPAC2019Importer.writers.shpwriter import create_writer
  from addons.RSUPAC2019Importer.writers.writerfacade import create_writer

  trace_remove()
  try:
    os.remove("/tmp/srupac2019.shp")
  except:
    pass
    
  taskManager = ToolsLocator.getTaskStatusManager()

  status = taskManager.createDefaultSimpleTaskStatus("SRU PAC")

  source = File(gvsig.getResource(__file__,"..","datos","test","RSU_PAC_2019_extra.xml"))
  source = File("/home/jjdelcerro/BDA_RSU_PAC19_1723072019_001.XML")
  target = File("/tmp/srupac2019.shp")
  
  parser = create_parser(status, source)
  writer = create_writer(status, target)

  writer.drop()
  writer.create()
  
  writer.edit()
  parser.parse(writer)
  writer.finishEditing()


def main(*args):
  #test()
  pass
  
