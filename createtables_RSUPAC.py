# encoding: utf-8


#
# Unicode characters table
# https://www.rapidtables.com/code/text/unicode-characters.html
#

"""
Tablas a crear en el esquema "public":
- RSUPAC2019_EXPEDIENTES
- RSUPAC2019_EXPLOTACIONES
- RSUPAC2019_ORIGEN_ANIMALES
- RSUPAC2019_AYUDA_SOL_AD
- RSUPAC2019_AYUDA_SOL_PDR

- RSUPAC2019_R10_PARCEAS
- RSUPAC2019_RECINTOS_SIGPAC (R10_Parcelas/LD_RecintosSIGPAC)
- RSUPAC2019_RECINTOS_SIGPAC_AD (R10_Parcelas/LD_RecintosSIGPAC/LD_Linea_AyudaSolAD)
- RSUPAC2019_RECINTOS_SIGPAC_PDR (R10_Parcelas/LD_RecintosSIGPAC/LD_Linea_AyudaSolPDR)
- RSUPAC2019_RECINTOS_SIGPAC_AS (R10_Parcelas/LD_RecintosSIGPAC/AyudaSecundario)
- RSUPAC2019_RECINTOS_SIGPAC_CH (R10_Parcelas/LD_RecintosSIGPAC/CultivosHorticolas)

"""

#
# ============================================
#
# Funcions de utilidad
#
from gvsig import geom

from org.gvsig.fmap.geom import Geometry

from org.gvsig.tools.dynobject import DynObjectValueItem

def setAvailableValues(attr, *values):
  vs = list()
  for v in values:
    vs.append(DynObjectValueItem(v[0], v[1]))
  attr.setAvailableValues(vs)
  

def add_relatedFeatures(ft, name, table, tablekey, tablecolumns, expression):
  x = ft.add( name, "List")\
    .setFeatureAttributeEmulator(expression)
  tags = x.getTags()
  tags.set("dynform.label.empty",True)
  tags.set("dynform.label.empty",True)
  tags.set("DAL.RelatedFeatures.Columns","/".join(tablecolumns))
  tags.set("DAL.RelatedFeatures.Table",table)
  tags.set("DAL.RelatedFeatures.Unique.Field.Name",tablekey)
  return x

def foreingkey(attr, table, code, label):
  attr.set("foreingkey",True)
  attr.set("foreingkey.table",table)
  attr.set("foreingkey.code",code)
  attr.set("foreingKey.Label",label)
  attr.set("foreingkey.closedlist",False)
  return attr
#
# ============================================
#
# Funcions asociadas a los tipos de datos del XSD
#

def add_TipoCampania(ft, name):
  # 4 digits
  x = ft.add( name, "Integer")\
    .setLabel(u"Campa\u00F1a")\
    .setDescription(u"El a\u00F1o que corresponda")
  return x 

def add_TipoIndicadorSN(ft, name):
  x = ft.add( name, "Boolean")
  return x 

def add_TipoAnyo(ft, name):
  # 4 digitos
  x = ft.add( name, "Integer")\
    .setLabel(u"A\u00F1o")
  return x 

def add_TipoCCAA(ft, name):
  x = ft.add( name, "String", 2)\
    .setLabel(u"C\u00F3d. CCAA")\
    .setShortLabel(u"CCAA")\
    .setDescription(u"Comunidad autonoma")
  setAvailableValues(x,
    ("01", u"01 - Andaluc\u00EDa"),
    ("02", u"02 - Arag\u00F3n"),
    ("03", u"03 - Principado de Asturias"),
    ("04", u"04 - Illes Balears"),
    ("05", u"05 - Canarias"),
    ("06", u"06 - Cantabria"),
    ("07", u"07 - Castilla La Mancha"),
    ("08", u"08 - Castilla y Le\u00F3n"),
    ("09", u"09 - Catalu\u00F1a"),
    ("10", u"10 - Extremadura"),
    ("11", u"11 - Galicia"),
    ("12", u"12 - Madrid"),
    ("13", u"13 - Regi\u00F3n de Murcia"),
    ("14", u"14 - Navarra"),
    ("15", u"15 - Pa\u00EDs Vasco"),
    ("16", u"16 - La Rioja"),
    ("17", u"17 - Comunidad Valenciana")
  )
  return x 

def add_TipoProvincia(ft, name):
  x = ft.add( name, "String", 2)\
    .setLabel(u"C\u00F3d. provincia")\
    .setDescription(u"C\u00F3digo INE de provincia")
  return x 

def add_TipoCentroReceptor(ft, name):
  # 3 digitos
  x = ft.add( name, "Integer")\
    .setLabel(u"C\u00F3d. centro receptor")\
    .setShortLabel(u"C\u00F3d. C.R.")\
    .setDescription(u"C\u00F3digo del centro receptor")
  return x 

def add_TipoNumExpdiente(ft, name):
  x = ft.add( name, "String", 20)\
    .setLabel(u"N\u00FAm. expediente")\
    .setDescription(u"N\u00FAmero de expediente")
  return x 

def add_TipoFecha(ft, name):
  x = ft.add( name, "Date")
  return x 

def add_TipoCIFNIF(ft, name):
  x = ft.add( name, "String", 9)\
    .setLabel(u"CIF/NIF")\
    .setDescription(u"CIF, NIF o NIE de hasta 9 caracteres")
  return x 

def add_TipoCIFNIFNIE(ft, name):
  x = ft.add( name, "String", 14)\
    .setLabel(u"CIF/NIF/NIE")\
    .setDescription(u"CIF, NIF o NIE de hasta 9 caracteres, o codigo de extrangero de hasta 14 caracteres")
  return x 

def add_TipoCIF(ft, name):
  x = ft.add( name, "String", 9)\
    .setLabel(u"CIF")\
    .setDescription(u"CIF de hasta 9 caracteres")
  return x 

def add_TipoNombreRazonSocial150(ft, name):
  x = ft.add( name, "String", 150)\
    .setLabel(u"Nombre")
  return x 

def add_TipoNombreRazonSocial90(ft, name):
  x = ft.add( name, "String", 150)\
    .setLabel(u"Nombre")\
    .setDescription(u"Nombre o razon social, o nombre de pasto")
  return x 

def add_TipoApellido(ft, name):
  x = ft.add( name, "String", 50)\
    .setLabel(u"Apellido")
  return x 

def add_TipoSexo(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Sexo")\
    .setDescription(u"Sexo: (F)emenino / (M)asculino / (I)ntersexual")
  setAvailableValues(x, 
    ( "F", u"F - Femenino"),
    ( "M", u"M - Masculino"),
    ( "I", u"I - Intersexual")
  )
  return x 

def add_TipoDireccion(ft, name):
  x = ft.add( name, "String", 300)\
    .setLabel(u"Direcci\u00F3n")\
    .setDescription(u"Direcci\u00F3n (calle o plaza)")
  return x 

def add_TipoLocalidad(ft, name):
  x = ft.add( name, "String", 300)\
    .setLabel(u"Localidad")  
  return x 

def add_TipoProvinciaMunicipio(ft, name):
  x = ft.add( name, "String", 5)\
    .setLabel(u"Municipio")\
    .setDescription(u"C\u00F3digo de provincia y municipio")
  return x 

def add_TipoCodPostal(ft, name):
  x = ft.add( name, "String", 5)\
    .setLabel(u"C\u00F3d. postal")\
    .setDescription(u"C\u00F3digo postal)")
  return x 

def add_TipoTelefono(ft, name):
  x = ft.add( name, "String", 9)\
    .setLabel(u"Telefono")
  return x 

def add_TipoEmail(ft, name):
  x = ft.add( name, "String", 90)
  x.setLabel(u"Correo electronico")
  x.setShortLabel(u"EMail")
  return x 

def add_TipoEntidadJuridica(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Entidad juridica")\
    .setDescription(u"Tipo de entidad juridica")
  setAvailableValues(x, 
    ( "1", u"1 - SAT"),
    ( "2", u"2 - Cooperativa"),
    ( "3", u"3 - Sociedad civil"),
    ( "4", u"4 - Comunidad de bienes"),
    ( "5", u"5 - Otras personas juridicas")
  )
  return x 

def add_TipoRegimenMatrimonial(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Regimen matrimonial")\
    .setShortLabel(u"Reg. matrimonial")\
    .setDescription(u"Regimen matrimonial")
  setAvailableValues(x, 
    ( "1", u"1 - Gananciales"),
    ( "2", u"2 - Separacion de bienes"),
    ( "3", u"3 - Participacion")
  )
  return x 

def add_TipoRelacionConTitular(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Relacion con titular")\
    .setShortLabel(u"Rel. titular")\
    .setDescription(u"Tipo de relacion con el titular")
  setAvailableValues(x, 
      ( "1", u"1 - El titular es jefe de la explotacion."),
      ( "2", u"2 - El jefe de la explotacion no es el titular, ni miembro de la familia del titular."),
      ( "3", u"3 - El jefe de la explotacion es conyuge del titular."),
      ( "4", u"4 - El jefe de la explotacion es familiar del titular.")
  )
  return x 

def add_TipoPorcTA(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"% tiempo anual")\
    .setShortLabel(u"% anual")\
    .setDescription(u"Porcentaje de tiempo anual dedicado al trabajo en la explotacion")
  setAvailableValues(x, 
    ("1", u"1 - 0 o menor que  25"), 
    ("2", u"2 - 25 o menor que  50"), 
    ("3", u"3 - 50 o menor que  75"), 
    ("4", u"4 - 75 o menor que 100"), 
    ("5", u"5 - a tiempo completo (= 100)")                     
  )
  return x 

def add_TipoFormAgraria(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Formacion agraria")\
    .setShortLabel(u"F. agraria")\
    .setDescription(u"Formacion agraria")
  setAvailableValues(x, 
    ("1", u"1 - Solo experiencia practica agraria."),
    ("2", u"2 - Cursos de formacion agraria."),
    ("3", u"3 - Formacion profesional agraria."),
    ("4", u"4 - Estudios universitarios y/o Superiores agrarios.")
  )
  return x 

def add_TipoIBAN(ft, name):
  x = ft.add( name, "String", 4)\
    .setLabel(u"Codigo IBAN")\
    .setShortLabel(u"IBAN")
  return x 

def add_TipoBancoSucursal(ft, name):
  x = ft.add( name, "String", 4)\
    .setDescription(u"Codigo de banco o sucursal")
  return x 

def add_TipoDC(ft, name):
  x = ft.add( name, "String", 2)\
    .setDescription(u"Digitos de control")
  return x 

def add_TipoCCC(ft, name):
  x = ft.add( name, "String", 10)\
    .setLabel(u"Cuenta corriente")\
    .setShortLabel(u"CCC")\
    .setDescription(u"Numero de cuenta corriente o libreta")
  return x 

def add_TipoCodREGEPA(ft, name):
  x = ft.add( name, "String", 10)\
    .setLabel(u"Codigo REGEPA")\
    .setShortLabel(u"REGEPA")\
    .setDescription(u"Codigo REGEPA")
  return x 

def add_TipoCodREGA(ft, name):
  x = ft.add( name, "String", 14)\
    .setLabel(u"Codigo REGA")\
    .setShortLabel(u"REGA")\
    .setDescription(u"Codigo REGA (ES999999999999)")
  return x 

def add_TipoIngresos(ft, name):
  x = ft.add( name, "Double")\
    .setLabel(u"Ingresos")\
    .setShortLabel(u"Ingresos")\
    .setDescription(u"Ingresos agrarios / no agrarios")
  return x 

def add_TipoNombreOI(ft, name):
  x = ft.add( name, "String", 60)\
    .setLabel(u"Nombre OIs")\
    .setShortLabel(u"OI")\
    .setDescription(u"Nombre de la OI")
  return x 

def add_TipoSuperficie(ft, name):
  x = ft.add( name, "Integer")\
    .setLabel(u"Superficie")\
    .setDescription(u"Superficie, numero entero expresado en areas")
  return x 

def add_TipoLineaAD(ft, name):
  x = ft.add( name, "String", 3)\
    .setLabel(u"Cod. linea ayuda AD")\
    .setShortLabel(u"AD")\
    .setDescription(u"Codigo de la linea de ayuda AD")
  setAvailableValues(x, 
    (   "1", u"001 Régimen de Pago Básico"),
    (   "2", u"002 Pago para prácticas beneficiosas para el clima y el medio ambiente (Greening)"),
    (   "6", u"006 Pago para jóvenes agricultores"),
    (   "9", u"009 Régimen de Pequeños agricultores"),
    ( "201", u"201 Ayuda asociada al cultivo del arroz"),
    ( "202", u"202 Ayuda asociada a los cultivos proteicos"),
    ( "203", u"203 Ayuda asociada a los frutos de cáscara y las algarrobas"),
    ( "204", u"204 Ayuda asociada a las legumbres de calidad"),
    ( "205", u"205 Ayuda asociada a la remolacha azucarera"),
    ( "206", u"206 Ayuda asociada al tomate para industria"),
    ( "207", u"207 Ayuda al algodón"),
    ( "301", u"301 Ayuda asociada vaca nodriza."),
    ( "302", u"302 Ayuda asociada vacuno de cebo"),
    ( "303", u"303 Ayuda asociada vacuno de leche"),
    ( "304", u"304 Ayuda asociada ovino"),
    ( "305", u"305 Ayuda asociada caprino"),
    ( "306", u"306 Ayuda asociada vacuno de leche derechos especiales"),
    ( "307", u"307 Ayuda asociada vacuno de cebo derechos especiales"),
    ( "308", u"308 Ayuda asociada ovino/caprino derechos especiales")
  )
  return x 

def add_TipoLineaADSecundario(ft, name):
  x = ft.add( name, "String", 3)\
    .setLabel(u"Cod. AD Secundario")\
    .setShortLabel(u"AD Secundario")\
    .setDescription(u"Codigo de la linea de ayuda solicitada en cultivo secundario")
  setAvailableValues(x, 
    ("202", u"Ayuda asociada a los cultivos proteicos"),
    ("204", u"Ayuda asociada a las legumbres de calidad"),
    ("205", u"Ayuda asociada a la remolacha azucarada")
  )
  return x 


def add_TipoLineaPDR(ft, name):
  x = ft.add( name, "String", 11)\
    .setLabel(u"Cod. linea PDR")\
    .setShortLabel(u"PDR")\
    .setDescription(u"Codigo de la linea de ayuda PDR")
  return x 

def add_TipoLineaAPI(ft, name):
  x = ft.add( name, "String", 11)\
    .setLabel(u"Cod. linea API")\
    .setShortLabel(u"API")\
    .setDescription(u"Codigo de la linea de ayuda de apicultura")
  return x 

def add_TipoNumeroOrden(ft, name):
  x = ft.add( name, "Integer")\
    .setLabel(u"Numero orden")\
    .setShortLabel(u"Num. orden")\
    .setDescription(u"Numero de orden")
  return x 

def add_TipoOPFH(ft, name):
  x = ft.add( name, "Integer")\
    .setLabel(u"Numero OPFH")\
    .setShortLabel(u"Num. OPFH")\
    .setDescription(u"Numero de la OPFH")
  return x 

def add_TipoSistemaExplotacion(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Sistema explotacion")\
    .setShortLabel(u"Sis. explo.")\
    .setDescription(u"Sistema de explotacion")
  setAvailableValues(x, 
    ("S", u"S - Secano"),
    ("R", u"R - Regadio")
  )
  return x 

def add_TipoRecintoCompleto(ft, name):
  x = ft.add( name, "Integer")\
    .setLabel(u"Recinto completo")\
    .setShortLabel(u"Rec. Compl.")\
    .setDescription(u"Tipo Recinto Completo")
  setAvailableValues(x, 
    (1, u"1 - Linea de declaracion ocupa toda la extension del recinto"),
    (0, u"0 - Linea de declaracion ocupa parte de la extension del recinto")
  )
  return x 
    
def add_TipoDestinoProduccion(ft, name):
  # campo 56
  x = ft.add( name, "String", 1)\
    .setLabel(u"Destino de la produccion")\
    .setShortLabel(u"Dest. prod.")\
    .setDescription(u"Destino de la produccion")
  setAvailableValues(x, 
    ("1", u"1 - Consumo en fresco"),
    ("2", u"2 - Procesamiento industrial"),
    ("3", u"3 - Semillas o plantulas con fines comerciales"),
    ("4", u"4 - Energias renovables"),
    ("5", u"5 - Abonado en verde")
  )
  return x 
  
def add_TipoSistCultivoHorticolas(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Sitema de cultivo")\
    .setShortLabel(u"Sist. cultivo")\
    .setDescription(u"Sistema de cultivo empleado")
  setAvailableValues(x, 
    ("1", u"1 - Aire libre"),
    ("2", u"2 - Malla"),
    ("3", u"3 - Cubierta bajo plastico o invernadero")
  )
  return x 
    
def add_TipoRecuentoArboles(ft, name):
  x = ft.add( name, "Integer")\
    .setLabel(u"Recuento de arboles")\
    .setShortLabel(u"Arboles")\
    .setDescription(u"Recuento de arboles (almendros, avellanos, algarrobos, castanios)")
  return x 
    
def add_TipoObservaciones(ft, name):
  x = ft.add( name, "String", 20)\
    .setLabel(u"Observaciones")\
    .setShortLabel(u"Observaciones")\
    .setDescription(u"Observaciones")
  return x 
    
def add_TipoCodigoMUP(ft, name):
  x = ft.add( name, "String", 10)\
    .setLabel(u"TipoCodigoMUP")\
    .setShortLabel(u"TipoCodigoMUP")\
    .setDescription(u"Codigo de pasto: Numero de MUP en el caso de los montes de utilidad publica si se dispone del mismo")
  return x 
    
def add_TipoRegimenTenencia(ft, name): 
  x = ft.add( name, "String", 1)\
    .setLabel(u"Regimen de tenencia")\
    .setShortLabel(u"Reg. tenencia")\
    .setDescription(u"Regimen de tTnencia")
  setAvailableValues(x, 
    ("1", u"1 - Propiedad"),
    ("2", u"2 - Arrendamiento"),
    ("3", u"3 - Aparceria"),
    ("4", u"4 - Usufructo"),
    ("5", u"5 - Asignacion de superficie por parte de un bien comunal"),
    ("6", u"6 - Aparceria comunal")
  )
  return x 

def add_TipoCAPDeclarado(ft, name): #todo labels
  x = ft.add( name, "Integer")\
    .setLabel(u"TipoCAPDeclarado")\
    .setShortLabel(u"TipoCAPDeclarado")\
    .setDescription(u"TipoCAPDeclarado")
  return x 

def add_TipoUsosSIGPAC(ft, name):
  x = ft.add( name, "String", 2)\
    .setLabel(u"Uso SIGPAC")\
    .setShortLabel(u"Uso SIGPAC")\
    .setDescription(u"Uso SIGPAC")
  setAvailableValues(x, 
    ("AG", u"AG - CORRIENTES Y SUPERFICIES DE AGUA"),
    ("CA", u"CA - VIALES"),
    ("CF", u"CF - CITRICOS - FRUTAL"),
    ("CI", u"CI - CITRICOS"),
    ("CS", u"CS - CITRICOS - FRUTAL DE CASCARA"),
    ("CV", u"CV - CITRICOS - VINIEDO"),
    ("ED", u"ED - EDIFICACIONES"),
    ("EP", u"EP - ELEMENTO DEL PAISAJE"),
    ("FF", u"FF - FRUTAL DE CASCARA - FRUTAL"),
    ("FL", u"FL - ASOCIACION FRUTAL DE CASCARA-OLIVAR"),
    ("FO", u"FO - FORESTAL"),
    ("FS", u"FS - FRUTAL DE CASCARA"),
    ("FV", u"FV - ASOCIACION FRUTAL DE CASCARA-VINIEDO"),
    ("FY", u"FY - FRUTAL"),
    ("IM", u"IM - IMPRODUCTIVOS"),
    ("IV", u"IV - INVERNADEROS Y CULTIVOS BAJO PLASTICO"),
    ("OC", u"OC - OLIVAR - CITRICOS"),
    ("OF", u"OF - ASOCIACION OLIVAR-FRUTAL"),
    ("OV", u"OV - OLIVAR"),
    ("PA", u"PA - PASTO CON ARBOLADO"),
    ("PR", u"PR - PASTO ARBUSTIVO"),
    ("PS", u"PS - PASTIZAL"),
    ("TA", u"TA - TIERRA ARABLE"),
    ("TH", u"TH - HUERTA"),
    ("VF", u"VF - ASOCIACION FRUTAL-VINIEDO"),
    ("VI", u"VI - VINIEDO"),
    ("VO", u"VO - ASOCIACION OLIVAR-VINIEDO"),
    ("ZC", u"ZC - ZONA CONCENTRADA NO REFLEJADA EN LA ORTOFOTO"),
    ("ZU", u"ZU - ZONA URBANA"),
    ("ZV", u"ZV - ZONA CENSURADA")
  )
  return x 

def add_TipoReferenciaCatastral(ft, name):
  x = ft.add( name, "String", 20)\
    .setLabel(u"Referencia catastral")\
    .setShortLabel(u"Ref. catastral")\
    .setDescription(u"Referencia Catastral")
  return x 
    
def add_TipoZona(ft, name):
  x = ft.add( name, "String", 2)\
    .setLabel(u"Zona")\
    .setShortLabel(u"Zona")\
    .setDescription(u"Zona")
  return x 
    
def add_TipoParcelaRecinto(ft, name):
  x = ft.add( name, "String", 5)\
    .setLabel(u"Recinto")\
    .setShortLabel(u"Recinto")\
    .setDescription(u"Recinto")
  return x 


def add_TipoAgregadoPoligono(ft, name):
  x = ft.add( name, "String", 3)\
    .setLabel(u"Agregado poligono")\
    .setShortLabel(u"Agregado poligono")\
    .setDescription(u"Agregado / Poligono")
  return x 
    
def add_TipoLineaDeclaracionRecinto(ft, name): #todo labels
  x = ft.add( name, "Integer")\
    .setLabel(u"Linea Declaracion Recinto")\
    .setShortLabel(u"Tipo semilla")\
    .setDescription(u"Tipo de semilla")
  return x 
    
def add_TipoSemilla(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"semilla utilizada")\
    .setShortLabel(u"Semilla")\
    .setDescription(u"Semilla utilizada")
  setAvailableValues(x, 
    ("C", u"C - Certificada"),
    ("R", u"R - Reempleo"),
    ("N", u"N - Dato no disponible")
  )
  return x
  
def add_TipoCicloCultivo(ft, name):
  x = ft.add( name, "String", 1)\
    .setLabel(u"Ciclo de cultivo")\
    .setShortLabel(u"Cod. producto")\
    .setDescription(u"Ciclo de cultivo")
  setAvailableValues(x, 
    ("I", u"I - Invierno"),
    ("P", u"P - Primavera"),
  )
  return x
  
def add_TipoActividadAgraria(ft, name):
  x = ft.add( name, "String", 2)\
    .setLabel(u"Actividad agraria realizada")\
    .setShortLabel(u"Act. agraria")\
    .setDescription(u"Actividad agraria realizada")
  setAvailableValues(x, 
    ( "1", u"01 - Produccion"),
    ( "2", u"02 - Laboreo"),
    ( "3", u"03 - Eliminacion de malas hierbas"),
    ( "4", u"04 - Mantenimiento de cultivos permanentes"),
    ( "5", u"05 - Pastoreo"),
    ( "6", u"06 - Desbroce"),
    ( "7", u"07 - Siega para mantenimiento"),
    ( "8", u"08 - Mantenimiento de drenajes"),
    ( "9", u"09 - Estercolado o fertilizacion"),
    ("10", u"10 - Mantenimiento/Establecimiento de una cubierta vegetal en barbechos"),
    ("11", u"11 - Siega para la produccion de hierba"),
  )
  return x

def add_TipoVariedad(ft, name):
  # pag 26 - circular  2
  x = ft.add( name, "String", 4)\
    .setLabel(u"Codigo de variedad")\
    .setShortLabel(u"Cod. variedad")\
    .setDescription(u"Codigo de variedad, especie, tipo o subcodigo")\
  # TODO 
  # necesidad de que ciertos valores son especificos de cada especie
  return x
  
def add_TipoProducto(ft, name):
  # pag 26 - circular  2
  x = ft.add( name, "String", 3)\
    .setLabel(u"Codigo del producto")\
    .setShortLabel(u"Cod. producto")\
    .setDescription(u"Codigo del producto")
  setAvailableValues(x, 
    ("001", u"TRIGO BLANDO"),
    ("002", u"TRITICUM SPELTA"),
    ("003", u"TRIGO DURO"),
    ("004", u"MAÍZ"),
    ("005", u"CEBADA"),
    ("006", u"CENTENO"),
    ("007", u"SORGO"),
    ("008", u"AVENA"),
    ("009", u"ALFORFON"),
    ("010", u"MIJO"),
    ("011", u"ALPISTE"),
    ("012", u"TRANQUILLON"),
    ("013", u"TRITICALE"),
    ("014", u"TRITORDEUM"),
    ("019", u"TEFF"),
    ("020", u"BARBECHO TRADICIONAL"),
    ("021", u"BARBECHO MEDIOAMBIENTAL ABANDONO 5 AÑOS "),
    ("023", u"BARBECHO MEDIOAMBIENTAL"),
    ("024", u"BARBECHO SIN PRODUCCIÓN"),
    ("025", u"ABANDONO 20 años"),
    ("334", u"BARBECHO CON ESPECIES MELÍFERAS "),
    ("033", u"GIRASOL"),
    ("034", u"SOJA"),
    ("035", u"COLZA"),
    ("036", u"CAMELINA"),
    ("040", u"GUISANTES"),
    ("041", u"HABAS"),
    ("043", u"ALTRAMUZ DULCE"),
    ("049", u"ALUBIAS"),
    ("050", u"GARBANZOS"),
    ("051", u"LENTEJAS"),
    ("052", u"VEZA"),
    ("053", u"YEROS"),
    ("060", u"ALFALFA"),
    ("061", u"ALHOLVA"),
    ("063", u"PASTOS de menos de 5 años"),
    ("067", u"ESPARCETA (Ver variedades)"),
    ("068", u"FESTUCA"),
    ("069", u"RAYGRAS PERENNE (Lolium perenne L. x boucheanum Kunth.)"),
    ("070", u"AGROSTIS"),
    ("071", u"ARRHENATHERUM"),
    ("072", u"DACTILO"),
    ("073", u"FLEO"),
    ("074", u"POA"),
    ("076", u"ZULLA"),
    ("077", u"TRÉBOL"),
    ("080", u"ARROZ"),
    ("081", u"ALGODÓN"),
    ("082", u"REMOLACHA"),
    ("083", u"TABACO"),
    ("085", u"LINO TEXTIL PARA FIBRA"),
    ("086", u"CAÑAMO PARA FIBRA"),
    ("087", u"CACAHUETE"),
    ("088", u"CARTAMO"),
    ("089", u"CHUFA"),
    ("090", u"REGALIZ"),
    ("091", u"FLORES"),
    ("092", u"ROMANESCU"),
    ("093", u"LINO NO TEXTIL"),
    ("096", u"ESPECIES AROMATICAS HERBÁCEAS"),
    ("097", u"SETAS"),
    ("098", u"PIMIENTO PARA PIMENTÓN"),
    ("099", u"PATATA"),
    ("121", u"BONIATO"),
    ("138", u"ADORMIDERA"),
    ("151", u"PUERROS"),
    ("152", u"PIMIENTO"),
    ("153", u"MELÓN"),
    ("154", u"BRÓCOLI"),
    ("155", u"LECHUGA"),
    ("156", u"SANDIA"),
    ("157", u"CEBOLLA"),
    ("158", u"APIO"),
    ("159", u"COLIRRABANO"),
    ("160", u"COLIFLOR"),
    ("162", u"BERENJENA"),
    ("163", u"CALABACIN"),
    ("164", u"ALCACHOFA"),
    ("165", u"PEPINO"),
    ("166", u"ACELGA"),
    ("167", u"CEBOLLETA"),
    ("168", u"CHALOTA"),
    ("169", u"AJO"),
    ("170", u"COL"),
    ("171", u"CHIRIVÍA"),
    ("172", u"REPOLLO"),
    ("173", u"COL ROJA O LOMBARDA"),
    ("174", u"COL MILAN"),
    ("175", u"BERZA"),
    ("176", u"COLES DE BRUSELAS"),
    ("177", u"ENDIVIA"),
    ("178", u"ZANAHORIA"),
    ("179", u"NABO"),
    ("180", u"JUDÍA"),
    ("181", u"ACHICORIA"),
    ("182", u"GUINDILLAS"),
    ("183", u"ESPINACA"),
    ("184", u"CARDO"),
    ("185", u"CALABAZA"),
    ("186", u"CALABAZA DEL PEREGRINO"),
    ("187", u"BORRAJA"),
    ("188", u"PEPINILLOS"),
    ("189", u"ESCAROLA"),
    ("190", u"RABANO"),
    ("191", u"BERRO"),
    ("192", u"FRAMBUESAS"),
    ("193", u"HUERTA"),
    ("194", u"CHAMPIÑON"),
    ("197", u"TOMATE"),
    ("198", u"TOMATE PARA TRANSFORMACIÓN"),
    ("219", u"FRESAS"),
    ("220", u"CAÑA DE AZUCAR"),
    ("222", u"QUINOA"),
    ("223", u"MISCANTHUS"),
    ("236", u"CAÑA COMÚN (ARUNDO DONAX)"),
    ("238", u"ALTRAMUZ"),
    ("239", u"ALMORTA"),
    ("240", u"TITARROS"),
    ("241", u"MEZCLA VEZA – AVENA"),
    ("242", u"MEZCLA VEZA-TRITICALE"),
    ("243", u"MEZCLA VEZA-TRIGO"),
    ("244", u"MEZCLA VEZA-CEBADA"),
    ("245", u"MEZCLA ZULLA – AVENA"),
    ("246", u"MEZCLA ZULLA – CEBADA"),
    ("247", u"CULTIVOS MIXTOS DE ESPECIES PRATENSES "),
    ("248", u"ALGARROBA"),
    ("249", u"ALVERJA"),
    ("250", u"ALBERJÓN"),
    ("251", u"AJEDREA"),
    ("252", u"CILANTRO"),
    ("253", u"ANÍS DULCE"),
    ("254", u"ENELDO"),
    ("255", u"MANZANILLA"),
    ("256", u"VALERIANA"),
    ("257", u"ARTEMISA"),
    ("258", u"GENCIANA"),
    ("259", u"HISOPO"),
    ("260", u"HINOJO"),
    ("261", u"PEREJIL"),
    ("262", u"AZAFRÁN"),
    ("263", u"TOMILLO"),
    ("264", u"ALBAHACA"),
    ("265", u"MELISA O TORONJIL"),
    ("266", u"MENTA"),
    ("267", u"ORÉGANO"),
    ("268", u"SALVIA"),
    ("269", u"PERIFOLLO"),
    ("270", u"ESTRAGÓN"),
    ("271", u"MEJORANA"),
    ("272", u"CALÉNDULA"),
    ("273", u"COMINO"),
    ("274", u"ESTEVIA"),
    ("275", u"HIPÉRICO"),
    ("276", u"HIERBABUENA"),
    ("277", u"VERBENA"),
    ("298", u"MEZCLA GUISANTE-CEBADA"),
    ("299", u"MEZCLA GUISANTE-AVENA"),
    ("302", u"MEZCLA EN MÁRGENES MULTIFUNCIONALES "),
    ("303", u"MEZCLA DE RESERVORIOS"),
    ("304", u"COL CHINA"),
    ("305", u"MECLA AVENA-TRIGO"),
    ("306", u"MEZCLA AVENA-CEBADA"),
    ("307", u"MEZCLA AVENA-TRITICALE"),
    ("308", u"AGRIMONIA"),
    ("309", u"BARDANA"),
    ("310", u"DIENTE DE LEÓN"),
    ("311", u"ENULA"),
    ("312", u"EQUINACEA"),
    ("313", u"GINSENG"),
    ("315", u"LLANTÉN"),
    ("316", u"MALVAVISCO"),
    ("317", u"MANZANILLA AMARGA"),
    ("318", u"MANZANILLA DULCE"),
    ("319", u"MILENRAMA"),
    ("320", u"POLEO"),
    ("321", u"RÁBANO NEGRO"),
    ("322", u"ROMPEPIEDRA"),
    ("323", u"TRAVALERA"),
    ("324", u"VARA DE ORO"),
    ("325", u"TRIGO KHORASAN"),
    ("326", u"MAÍZ DULCE"),
    ("327", u"REMOLACHA DE MESA"),
    ("328", u"PASTO DEL SUDÁN"),
    ("329", u"AMARANTO"),
    ("330", u"ELEMENTO DEL PAISAJE"),
    ("332", u"MOSTAZA"),
    ("333", u"PORTAINJERTOS DE VID"),
    ("336", u"MEZCLA ALGARROBAS-AVENA"),
    ("337", u"MEZCLA ALGARROBAS-CEBADA"),
    ("338", u"MEZCLA VEZA-RAYGRASS"),
    ("339", u"MEZCLA YEROS-AVENA"),
    ("340", u"MEZCLA YEROS-CEBADA"),
    ("341", u"SILPHIUM"),
    ("342", u"OTRAS MEZCLAS CON PREDOMINANCIA CFN "),
    ("350", u"RASTROJERAS"),
    ("700", u"HECTÁREAS DE AGROSILVICULTURA QUE RECIBAN O HAYAN RECIBIDO AYUDAS DEL REGLAMENTO No 1698/2005 Y/O DEL REGLAMENTO No 1305/2013"),
    ("750", u"SUPERFICIES VINCULADAS A LA DIRECTIVA 92/43/CEE "),
    ("900", u"SINAPIS ALBA"),
    ("901", u"BRASSICA CARINATA"),
    ("902", u"BRASSICA JUNCEA"),
    ("903", u"OTRAS CRUCÍFERAS"),
    ("904", u"CROTALARIA JUNCEA"),
    ("78", u"RAYGRAS ANUAL (Lolium multiflorum LAM. And hybrids) "),
    ("139", u"HIERBA CINTA (Phalaris arundinacea L.)"),
    ("140", u"ABACA ALIAS MANILA (Musa textilis Née) "),
    ("141", u"KENAF (Hibiscus cannabinus L.)"),
    ("084", u"LÚPULO"),
    ("101", u"OLIVAR"),
    ("102", u"VIÑEDO VINIFICACION"),
    ("103", u"UVA DE MESA"),
    ("104", u"ALMENDROS"),
    ("105", u"MELOCOTONEROS"),
    ("106", u"NECTARINOS"),
    ("107", u"ALBARICOQUEROS"),
    ("108", u"PERALES"),
    ("109", u"MANZANOS"),
    ("110", u"CEREZOS"),
    ("111", u"CIRUELOS"),
    ("112", u"NOGALES"),
    ("113", u"OTROS FRUTALES"),
    ("117", u"CASTAÑOS"),
    ("118", u"ESPECIES AROMATICAS LEÑOSAS"),
    ("119", u"VIVEROS"),
    ("120", u"VIÑA – OLIVAR"),
    ("122", u"ALGARROBO"),
    ("123", u"AVELLANO"),
    ("124", u"PISTACHO"),
    ("125", u"FRUTOS DE CÁSCARA"),
    ("201", u"PLATERINA"),
    ("202", u"PARAGUAYO"),
    ("203", u"ENDRINO O ARAÑÓN"),
    ("204", u"CLEMENTINAS"),
    ("205", u"SATSUMAS"),
    ("206", u"NARANJO"),
    ("207", u"LIMONERO"),
    ("208", u"POMELO"),
    ("209", u"MANDARINO"),
    ("210", u"MANDARINO HÍBRIDO"),
    ("211", u"MEMBRILLO"),
    ("212", u"KIWI"),
    ("213", u"CAQUI o PALOSANTO"),
    ("214", u"NISPERO"),
    ("215", u"GROSELLA"),
    ("216", u"ARÁNDANO"),
    ("217", u"GRANADO"),
    ("218", u"HIGUERA"),
    ("221", u"UVA PASA"),
    ("226", u"OPUNTIA"),
    ("235", u"JATROPHA"),
    ("237", u"SUPERFICIES FORESTALES DE ROTACIÓN CORTA"),
    ("278", u"FRUTOS DEL BOSQUE"),
    ("279", u"ESPÁRRAGOS"),
    ("280", u"TRUFA"),
    ("281", u"LAVANDA"),
    ("282", u"LAVANDÍN"),
    ("283", u"ALCAPARRA"),
    ("284", u"AJENJO"),
    ("285", u"ESPLIEGO"),
    ("286", u"HELICRISO"),
    ("287", u"HIERBALUISA"),
    ("288", u"ROMERO"),
    ("289", u"SANTOLINA"),
    ("290", u"ALOE VERA"),
    ("291", u"CAFÉ"),
    ("292", u"GROSELLA NEGRA"),
    ("330", u"ELEMENTO DEL PAISAJE"),
    ("331", u"MORINGA"),
    ("335", u"CABECERA DE CULTIVO PERMANENTE"),
    ("909", u"NASHI"),
    ("142", u"YUTE (Corchorus capsularis L.)"),
    ("143", u"SISAL (Agave sisalana Perrine)"),
    ("343", u"AGUACATE (Ver variedades)"),
    ("344", u"MANGO (Ver variedades)"),
    ("345", u"CHIRIMOYO (Ver variedades)"),
    ("346", u"PAPAYA (Ver variedades)"),
    ("347", u"MORERA (Ver variedades)"),
    ("348", u"VIÑA- FRUTAL"),
    ("349", u"OLIVAR-FRUTAL"),
    ("910", u"LITCHI"),
    ("911", u"KUMQUAT"),
    ("912", u"LIMEQUAT"),
    ("913", u"MANO DE BUDA"),
    ("914", u"CAVIAR CÍTRICO/ FINGER LIME"),
    ("915", u"LIMA"),
    ("062", u"PASTOS PERMANENTES DE 5 O MÁS AÑOS"),
    ("064", u"PASTIZAL DE 5 O MÁS AÑOS"),
    ("065", u"PASTO ARBUSTIVO DE 5 O MÁS AÑOS"),
    ("066", u"PASTO ARBOLADO DE 5 O MÁS AÑOS"),
    ("028", u" RETIRADA FORESTACIÓN"),
    ("114", u"SUPERFICIES FORESTALES MADERABLES"),
    ("115", u"OTRAS SUPERFICIES FORESTALES"),
    ("116", u"CHOPOS"),
    ("200", u"PAULOWNIA"),
    ("224", u"LEUCAENA"),
    ("225", u"EUCALYPTUS"),
    ("227", u"SALIX"),
    ("228", u"ACACIA"),
    ("229", u"AILANTHUS"),
    ("230", u"ROBINIA"),
    ("231", u"GLEDITSIA"),
    ("232", u"JACARANDA"),
    ("233", u"PHYTOLACCA"),
    ("234", u"CASTAÑO (FORESTAL)"),
    ("293", u"ROBLE"),
    ("294", u"HAYA"),
    ("295", u"ALCORNOQUE"),
    ("296", u"ABETO"),
    ("297", u"ENEBRO"),
    ("300", u"SABINA"),
    ("301", u"PINSAPO"),
    ("400", u"FORESTACIONES VINCULADAS AL REGLAMENTO 2080/1992"),
    ("500", u"FORESTACIONES VINCULADAS AL REGLAMENTO No 1257/1999"),
    ("600", u"FORESTACIONES VINCULADAS AL REGLAMENTO No 1698/2005"),
    ("800", u"FORESTACIONES VINCULADAS AL REGLAMENTO No 1305/2013"),
    ("850", u"OTRAS SUPERFICIES FORESTALES-VUELO"),
    ("144", u"PINOS PIÑONEROS"),
    ("145", u"RESTO DE PINOS (NO PIÑONEROS)"),
    ("146", u"ARBOLES DE NAVIDAD"),
    ("150", u"OTRAS UTILIZACIONES NO AGRARIAS NI FORESTALES")

  )
  return x 
  
def add_TipoCoordenada(ft, name):
  x = ft.add( name, "Double")\
    .setLabel(u"Coordenada")\
    .setShortLabel(u"Coordenada")\
    .setDescription(u"Coordenada")
  return x 
    
#
# ============================================
#
# Funcions de inicializacion de los FeatureTypes
# de las tablas a crear.
#

def add_fields_RSUPAC2019_EXPLOTACIONES(ft):
  ft.setLabel("RSU PAC 2019 - Explotaciones")

  # RSU/Solicitud/OtrosDatos/Explotaciones
  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsIndexed(True)\
    .setLabel("Expediente")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_EXPEDIENTES")\
    .set("foreingkey.code","NumExpediente")\
    .set("foreingKey.Label","FORMAT('%s %s %s',NumExpediente,CodPostal_Solicitante, ID_Solicitante)")\
    .set("foreingkey.closedlist",False)

  add_TipoCodREGA(ft, "CodREGA")

def add_fields_RSUPAC2019_ORIGEN_ANIMALES(ft):
  ft.setLabel("RSU PAC 2019 - Explotaciones de origen animal")

  # RSU/Solicitud/OtrosDatos/OrigenAnimales
  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsIndexed(True)\
    .setLabel("Expediente")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_EXPEDIENTES")\
    .set("foreingkey.code","NumExpediente")\
    .set("foreingKey.Label","FORMAT('%s %s %s',NumExpediente,CodPostal_Solicitante, ID_Solicitante)")\
    .set("foreingkey.closedlist",False)
  add_TipoCodREGA(ft, "CodREGA")

def add_fields_RSUPAC2019_AYUDA_SOL_AD(ft):
  ft.setLabel("RSU PAC 2019 - Ayudas solicitadas AD")

  # RSU/Solicitud/ResumenSol/Linea_AyudaSolAD
  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsIndexed(True)\
    .setLabel("Expediente")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_EXPEDIENTES")\
    .set("foreingkey.code","NumExpediente")\
    .set("foreingKey.Label","FORMAT('%s %s %s',NumExpediente,CodPostal_Solicitante, ID_Solicitante)")\
    .set("foreingkey.closedlist",False)
  add_TipoLineaAD(ft, "Codigo_lineaAD")\
    .setLabel(u"Linea de ayuda AD solicitada")\
    .setShortLabel(u"AD")\
    .setDescription("Código línea de ayuda solicitada")
  add_TipoSuperficie(ft, "SupDeclarada_LineaAD")\
    .setDescription("Superficie para cada uno de los regímenes de ayuda. Número entero expresado en áreas.")

def add_fields_RSUPAC2019_AYUDA_SOL_PDR(ft):
  ft.setLabel("RSU PAC 2019 - Ayudas solicitadas PDR")

  # RSU/Solicitud/ResumenSol/Linea_AyudaSolPDR
  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsIndexed(True)\
    .setLabel("Expediente")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_EXPEDIENTES")\
    .set("foreingkey.code","NumExpediente")\
    .set("foreingKey.Label","FORMAT('%s %s %s',NumExpediente,CodPostal_Solicitante, ID_Solicitante)")\
    .set("foreingkey.closedlist",False)
  add_TipoLineaPDR(ft, "Codigo_lineaPDR")\
    .setLabel(u"Linea de ayuda PDR solicitada")\
    .setShortLabel(u"PDR")\
    .setDescription("Código de la línea de ayuda PDR. Se consignarán las medidas según la codificación indicada en el Documento de codificación 2019 de medidas de Desarrollo Rural.")


def add_fields_RSUPAC2019_EXPEDIENTES(ft):
  ft.setLabel("RSU PAC 2019 - Expedientes")
  
  tags = ft.getTags()
  tags.set("dynform.width",700)
  
  # RSU
  add_TipoCampania(ft, "Ano") 
  add_TipoCCAA(ft, "CA_Expediente")
  add_TipoProvincia(ft, "ProvExpediente")
  add_TipoCentroReceptor(ft, "CRExpediente")
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsPrimaryKey(True)\
    .setLabel("Num. expediente")
  add_TipoFecha(ft, "Fregistro")\
    .setLabel("Fecha registro")\
    .setShortLabel("F. registro")
  add_TipoFecha(ft, "Fmodificacion")\
    .setLabel("Fecha modificacion")\
    .setShortLabel("F. modificacion")

  # RSU/Solicitante
  add_TipoCIFNIF(ft, "ID_Solicitante")\
    .getTags().set("dynform.separator","Solicitante")
  add_TipoNombreRazonSocial150(ft, "Nombre_Solicitante")
  add_TipoApellido(ft, "Apellido1_Solicitante")\
    .setLabel("Apellido 1")
  add_TipoApellido(ft, "Apellido2_Solicitante")\
    .setLabel("Apellido 2")
  add_TipoFecha(ft, "Fnacimiento_Solicitante")\
    .setLabel("fecha nacimiento")\
    .setShortLabel("F. nacimiento")
  add_TipoSexo(ft, "Sexo_Solicitante") 
  add_TipoDireccion(ft, "Direccion_Solicitante")
  add_TipoLocalidad(ft, "Localidad_Solicitante")
  add_TipoProvinciaMunicipio(ft, "CodMunicipio_Solicitante")
  add_TipoCodPostal(ft, "CodPostal_Solicitante")
  add_TipoTelefono(ft, "Tfno_Solicitante")\
    .setLabel("Telfono fijo")\
    .setShortLabel("Telf. fijo")
  add_TipoTelefono(ft, "TfnoMovil_Solicitante")\
    .setLabel("Telefono movil")\
    .setShortLabel("Telf. movil")
  add_TipoEmail(ft, "email_Solicitante")
  add_TipoEntidadJuridica(ft, "Tipo_EJ_Solicitante")
  add_TipoIndicadorSN(ft, "TitComp_Solicitante")

  # RSU/Solicitud/Conyuge
  add_TipoNombreRazonSocial150(ft, "Nombre_Conyuge_Solicitud")\
    .setShortLabel("Nombre (conyugue)")\
    .getTags().set("dynform.separator","Solicitud - Conyuge")
  add_TipoApellido(ft, "Apellido1_Conyuge_Solicitud")\
    .setLabel("Apellido 1")\
    .setShortLabel("Apellido 1 (conyugue)")
  add_TipoApellido(ft, "Apellido2_Conyuge_Solicitud")\
    .setLabel("Apellido 2")\
    .setShortLabel("Apellido 2 (conyugue)")
  add_TipoIndicadorSN(ft, "Extran_Conyuge_Solicitud")\
    .setShortLabel("Extranjero (conyugue)")
  add_TipoCIFNIFNIE(ft, "ID_Conyuge_Solicitud")\
    .setShortLabel("CIF (conyugue)")
  add_TipoRegimenMatrimonial(ft, "RegMatrimonial_Conyuge_Solicitud")

  # RSU/Solicitud/Representante
  add_TipoNombreRazonSocial150(ft, "Nombre_Repres_Solicitud")\
    .setShortLabel("Nombre (Repr)")\
    .getTags().set("dynform.separator","Solicitud - Representante")
  add_TipoApellido(ft, "Apellido1_Repres_Solicitud")\
    .setLabel("Apellido 1")\
    .setShortLabel("Appellido 1 (Repr)")
  add_TipoApellido(ft, "Apellido2_Repres_Solicitud")\
    .setLabel("Apellido 2")\
    .setShortLabel("Apellido 2 (Repr)")
  add_TipoIndicadorSN(ft, "Extran_Repres_Solicitud")\
    .setShortLabel("Extranjero (Repr)")
  add_TipoCIFNIFNIE(ft, "ID_Repres_Solicitud")\
    .setShortLabel("CIF (Repr)")

  # RSU/Solicitud/RespJuridica
  add_TipoIndicadorSN(ft, "SolGrupoEmpresarial_Solicitud")\
    .setShortLabel("Gr.Empresarial (RespJur)")\
    .getTags().set("dynform.separator","Solicitud - Grupo empresarial")

  # RSU/Solicitud/JefeExplotacion
  add_TipoRelacionConTitular(ft, "Relacion_Con_Titular_JE_Solicitud")\
    .setShortLabel("Rel. titular (JE)")\
    .getTags().set("dynform.separator","Solicitud - Jefe explotacion")
  add_TipoIndicadorSN(ft, "Comparte_resp_gestion_JE_Solicitud")\
    .setShortLabel("Comp. Gestion (JE)")
  add_TipoIndicadorSN(ft, "Extran_JE_Solicitud")\
    .setShortLabel("Extrangero (JE)")
  add_TipoCIFNIFNIE(ft, "ID_JE_Solicitud")\
    .setShortLabel("CIF (JE)")
  add_TipoNombreRazonSocial150(ft, "Nombre_JE_Solicitud")\
    .setShortLabel("Nombre (JE)")
  add_TipoApellido(ft, "Apellido1_JE_Solicitud")\
    .setLabel("Apellido 1")\
    .setShortLabel("Apellido 1 (JE)")
  add_TipoApellido(ft, "Apellido2_JE_Solicitud")\
    .setLabel("Apellido 2")\
    .setShortLabel("Apellido 2 (JE)")
  add_TipoFecha(ft, "Fnacimiento_JE_Solicitud")\
    .setLabel("Fecha nacimiento")\
    .setShortLabel("F. naci.(JE)")
  add_TipoSexo(ft, "Sexo_JE_Solicitud")
  add_TipoTelefono(ft, "Tfno_JE_Solicitud")\
    .setLabel("Telefono fijo")\
    .setShortLabel("Telf. fijo (JE)")
  add_TipoTelefono(ft, "TfnoMovil_JE_Solicitud")\
    .setLabel("Telefono movil")\
    .setShortLabel("Telf. movil (JE)")
  add_TipoEmail(ft, "email_JE_Solicitud")\
    .setShortLabel("email (JE)")
  add_TipoPorcTA(ft, "PorcTA_JE_Solicitud")\
    .setShortLabel("% TA (JE)")
  add_TipoAnyo(ft, "AnoInicio_JE_Solicitud")\
    .setShortLabel(u"A\u00F1o ini. (JE)")\
    .setDescription(u"A\u00F1o comienzo trabajo en explotación")
  add_TipoFormAgraria(ft, "FormAgraria_JE_Solicitud")\
    .setShortLabel("F.agraria (JE)")
  add_TipoIndicadorSN(ft, "CursosPerfe_JE_Solicitud")\
    .setLabel(u"Cursos perfeccionamiento")\
    .setShortLabel(u"Curs. Perf. (JE)")\
    .setDescription(u"Cursos de perfeccionamiento realizados durante los últimos doce meses")
  
  # RSU/Solicitud/DatosBancarios
  add_TipoIBAN(ft, "IBAN_DB_Solicitud")\
    .getTags().set("dynform.separator","Solicitud - Datos bancarios")
  add_TipoBancoSucursal(ft, "Banco_DB_Solicitud")\
    .setLabel(u"Banco")
  add_TipoBancoSucursal(ft, "Sucursal_DB_Solicitud")\
    .setLabel(u"Sucursal")
  add_TipoDC(ft, "DC_DB_Solicitud")
  add_TipoCCC(ft, "CCC_DB_Solicitud")

  # RSU/Solicitud/OtrosDatos
  add_TipoCodREGEPA(ft, "CodREGEPA_OD_Solicitud")\
    .getTags().set("dynform.separator","Solicitud - Otros")
  add_TipoIndicadorSN(ft, "VentaDirecta_OD_Solicitud")\
    .setDescription(u"Venta Directa. marcar exclusivamente por aquellos solicitantes que realizan venta directa de su producción agraria al consumidor (RD 9/2015 de 16 de enero)")
  
  # RSU/Solicitud/OtrosDatos/Explotaciones/CodREGA
  add_relatedFeatures(ft, 
    "Explotaiones_OD_Solicitud", 
    "RSUPAC2019_EXPEDIENTES_EXPLOTACIONES", 
    "ID", 
    ("ID", "CodREGA"), 
    "FEATURES('RSUPAC2019_EXPEDIENTES_EXPLOTACIONES',FORMAT('NumExpediente = ''%s''',NumExpediente))"
  )\
  .setGroup(u"REGA Explotacion")
  
  add_TipoIngresos(ft, "IA_OD_Solicitud")
  add_TipoIndicadorSN(ft, "PrimeraAA_OD_Solicitud")\
    .setLabel(u"Primera vez del solicitante")\
    .setDescription(u"Solicitante que se incorpora por primera vez a la actividad agraria. Marcar exclusivamente por aquellos solicitantes que se incorporen a la actividad agraria.")

  add_TipoIndicadorSN(ft, "JovenGan_OD_Solicitud")\
    .setLabel(u"Joven ganadero")\
    .setShortLabel(u"Joven G.")
  add_TipoIndicadorSN(ft, "NuevoGan_OD_Solicitud")\
    .setLabel(u"Nuevo ganadero")\
    .setShortLabel(u"Nuevo G.")

  # RSU/Solicitud/OtrosDatos/OrigenAnimales/CodREGA
  add_relatedFeatures(ft, 
    "OrigenAnimales_OD_Solicitud", 
    "RSUPAC2019_ORIGEN_ANIMALES", 
    "ID", 
    ("ID", "CodREGA"), 
    "FEATURES('RSUPAC2019_ORIGEN_ANIMALES',FORMAT('NumExpediente = ''%s''',NumExpediente))"
  )\
  .setGroup(u"REGA Explotacion (Orig. animales)")\
  .setDescription(u"Código REGA de la explotación origen de los animales")
  
  add_TipoOPFH(ft, "OPFH_OD_Solicitud")
  add_TipoCCAA(ft, "CA_OPFH_OD_Solicitud")\
    .setLabel(u"Comunidad autónoma de la OPFH")\
    .setShortLabel(u"CCAA OPFH")
  add_TipoNombreRazonSocial150(ft, "Razon_Social_OPFH_OD_Solicitud")\
    .setLabel(u"Razón social de la OPFH")\
    .setShortLabel(u"R.S. OPFH")
  add_TipoNombreOI(ft, "OI_algodon_OD_Solicitud")\
    .setLabel(u"OI en el caso de 'algodón'")\
    .setShortLabel(u"OI algodon")
  add_TipoCIFNIF(ft, "CIF_OI_OD_Solicitud")\
    .setLabel(u"CIF de la OI")\
    .setShortLabel(u"CIF OI")
  add_TipoCIFNIF(ft, "NIF_CIF_integradora_OD_Solicitud")\
    .setLabel(u"NIF de la integradora")\
    .setShortLabel(u"NIF Integradora")
  add_TipoIngresos(ft, "IA_integrado_OD_Solicitud")\
    .setLabel(u"Ingresos agrarios del integrado")\
    .setShortLabel(u"Ing.Agr.Integrado")
  add_TipoIndicadorSN(ft, "Cebadero_comunitario_OD_Solicitud")\
    .setLabel(u"Marca de cebadero comunitario")\
    .setShortLabel(u"Cebadero Com.")
  add_TipoCIFNIF(ft, "CIF_cebadero_comunitario_OD_Solicitud")\
    .setLabel(u"CIF del cerbadero comunitario")\
    .setShortLabel(u"CIF Ceb.Com.")

  # RSU/Solicitud/ResumenSol
  add_TipoSuperficie(ft, "SupDeclarada_RS_Solicitud")\
    .setLabel(u"Superfície total explotación declarada")\
    .setShortLabel(u"Superfície")\
    .setDescription(u"Superficie total de la explotación: número entero expresado en áreas")\
    .getTags().set("dynform.separator",u"Solicitud - Resumen de la declaracion")
  add_TipoSuperficie(ft, "PP5anos_RS_Solicitud")\
    .setLabel(u"Pastos permanentes ≥ 5 años")\
    .setShortLabel(u"Pastos perm.")\
    .setDescription(u"Superficie declarada de Pastos permanentes de ≥ de 5 años: número entero expresado en áreas.")
  add_TipoSuperficie(ft, "Otras_supforrajeras_RS_Solicitud")\
    .setLabel(u"Otras superficies forrajeras")\
    .setShortLabel(u"Otras superf.")\
    .setDescription(u"Otras superficies forrajeras carga ganadera")

  # RSU/Solicitud/ResumenSol/Linea_AyudaSolAD
  add_relatedFeatures(ft, 
    "Linea_AyudaSolAD_RS_Solicitud", 
    "RSUPAC2019_AYUDA_SOL_AD", 
    "ID", 
    ("ID", "Codigo_LineaAD", "SupDeclarada_LineaAD"), 
    "FEATURES('RSUPAC2019_AYUDA_SOL_AD',FORMAT('NumExpediente = ''%s''',NumExpediente))"
  )\
  .setGroup("Ayudas AD")


  # RSU/Solicitud/ResumenSol/Linea_AyudaSolPDR
  add_relatedFeatures(ft, 
    "Linea_AyudaSolPDR_RS_Solicitud", 
    "RSUPAC2019_AYUDA_SOL_PDR", 
    "ID", 
    ("ID", "Codigo_LineaPDR"), 
    "FEATURES('RSUPAC2019_AYUDA_SOL_PDR',FORMAT('NumExpediente = ''%s''',NumExpediente))"
  )\
  .setGroup("Ayudas PDR")


  # RSU/R10_parcelas
  add_relatedFeatures(ft, 
    "R10_Parcelas", 
    "RSUPAC2019_R10_PARCELAS", 
    "ID_PARCELA", 
    ("NumExpediente", "PA_NumOrden", "PA_SupTotalDec", "PA_Producto"), 
    "FEATURES('RSUPAC2019_R10_PARCEAS',FORMAT('NumExpediente = ''%s''',NumExpediente))"
  )\
  .setGroup("Parcelas")


def add_fields_RSUPAC2019_R10_PARCELAS(ft):
  ft.setLabel("RSU PAC 2019 - R10 Parcelas")
  
  tags = ft.getTags()
  tags.set("dynform.width",500)
  
  # RSU/Parcelas/R10_Parcelas
  # pag 12 - circular 2
  
  # ID_PARCELA = "%20.20s%05d" % (NumExpediente,PA_NumOrden)
  ft.add("ID_PARCELA", "String", 25)\
    .setIsPrimaryKey(True)\
    .setLabel("Id. parcela")
  add_TipoNumExpdiente(ft, "NumExpediente")\
    .setIsIndexed(True)\
    .setLabel("Expediente")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_EXPEDIENTES")\
    .set("foreingkey.code","NumExpediente")\
    .set("foreingKey.Label","FORMAT('%s %s %s',NumExpediente,CodPostal_Solicitante, ID_Solicitante)")\
    .set("foreingkey.closedlist",False)

  add_TipoNumeroOrden(ft, "PA_NumOrden")\
    .setLabel(u"Numero de Orden")\
    .setShortLabel(u"Num. Orden")\
    .setDescription(u"Numero de orden formateado con ceros a la izquierda.")
  add_TipoSuperficie(ft, "PA_SupTotalDec")\
    .setLabel(u"Superficie total declarada")\
    .setShortLabel(u"Sup. total declarada")\
    .setDescription(u"Superficie total declarada de la Parcela Agrícola: Número entero expresado en áreas.")
  add_TipoSistemaExplotacion(ft, "PA_SistemaExplotacion")\
    .setLabel(u"Sistema de explotacion")\
    .setShortLabel(u"Sis. explotacion")\
    .setDescription(u"Sistema de explotacion")
  add_TipoProducto(ft, "PA_Producto")\
    .setLabel(u"Producto")\
    .setShortLabel(u"Producto")\
    .setDescription(u"Codigo del producto")
  add_TipoVariedad(ft, "PA_Variedad")\
    .setLabel(u"Variedad/Especie/Tipo/Subcódigo")\
    .setShortLabel(u"Variedad")\
    .setDescription(u"Codigo de variedad, especie, tipo o subcodigo")
  add_TipoCicloCultivo(ft, "PA_Ciclo")\
    .setLabel(u"Ciclo de cultivo")\
    .setShortLabel(u"Ciclo cultivo")\
    .setDescription(u"Ciclo de cultivo")
  add_TipoActividadAgraria(ft, "AA_realizada")\
    .setLabel(u"Actividad agraria realizada")\
    .setShortLabel(u"Act. agraria")\
    .setDescription(u"Actividad agraria realizada")
  add_TipoIndicadorSN(ft, "ProdEcologica")\
    .setLabel(u"Produccion ecologica")\
    .setShortLabel(u"Prod. ecologica")\
    .setDescription(u"Produccion ecologica")
  add_TipoSemilla(ft, "TipSemilla")\
    .setLabel(u"Tipo de semilla")\
    .setShortLabel(u"Tip. semilla")\
    .setDescription(u"Tipo de semilla")

  # RSU/R10_parcelas/LD_RecintoSIGPAC
  add_relatedFeatures(ft, 
    "LD_RecintoSIGPAC", 
    "RSUPAC2019_RECINTOS_SIGPAC", 
    "ID_RECINTO", 
    ("ID_RECINTO", "ID_PARCELA", "PA_NumOrden", "RefCatastral", "ProvMuni"), 
    "FEATURES('RSUPAC2019_RECINTOS_SIGPAC',FORMAT('ID_PARCELA = ''%s''',ID_PARCELA))"
  )\
  .setGroup("Parcelas")


def add_fields_RSUPAC2019_RECINTOS_SIGPAC(ft):
  ft.setLabel("RSU PAC 2019 - Recintos SIGPAC")
  
  tags = ft.getTags()
  tags.set("dynform.width",700)
  
  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC
  ft.add("ID_RECINTO", "Integer")\
    .setIsPrimaryKey(True)\
    .setLabel("Id. recinto")
  ft.add("ID_PARCELA", "Integer")\
    .setIsIndexed(True)\
    .setLabel("Parcela")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_R10_PARCELAS")\
    .set("foreingkey.code","ID_PARCELA")\
    .set("foreingKey.Label","FORMAT('%s %f %s %s',ID_PARCELA,PA_SupTotalDec, PA_Producto, PA_Variedad)")\
    .set("foreingkey.closedlist",False)
    
  add_TipoLineaDeclaracionRecinto(ft, "LineaDeclaracion")\
    .setLabel(u"Linea de Declaracion de Recinto")\
    .setShortLabel(u"Lin. Recinto")\
    .setDescription(u"Linea de Declaracion de Recinto")
  add_TipoSuperficie(ft, "SupRecintoDec")\
    .setLabel(u"Superficie decladara en el recinto")\
    .setShortLabel(u"Sup. recinto")\
    .setDescription(u"Superficie de la Parcela Agricola declarada en el recinto")
  add_TipoProvinciaMunicipio(ft, "ProvMuni")\
    .setLabel(u"Provincia y municipio")\
    .setShortLabel(u"Prov. y municipo")\
    .setDescription(u"Codigo de provincia (dos posiciones) y codigo de municipio (tres posiciones) siguiendo la codificacion catastral")
  add_TipoAgregadoPoligono(ft, "Agregado")\
    .setLabel(u"Agregado")\
    .setShortLabel(u"Agregado")\
    .setDescription(u"Agregado. Formateados con ceros a la izquierda")
  add_TipoZona(ft, "Zona")\
    .setLabel(u"Zona")\
    .setShortLabel(u"Zona")\
    .setDescription(u"Zona. Formateados con ceros a la izquierda")
  add_TipoAgregadoPoligono(ft, "Poligono")\
    .setLabel(u"Poligono")\
    .setShortLabel(u"Poligono")\
    .setDescription(u"Poligono. Formateados con ceros a la izquierda")
  add_TipoParcelaRecinto(ft,  "Parcela")\
    .setLabel(u"Parcela")\
    .setShortLabel(u"Parcela")\
    .setDescription(u"Parcela. Formateados con ceros a la izquierda")
  add_TipoParcelaRecinto(ft,  "Recinto")\
    .setLabel(u"Recinto")\
    .setShortLabel(u"Recinto")\
    .setDescription(u"Recinto. Formateados con ceros a la izquierda")
  add_TipoReferenciaCatastral(ft, "RefCatastral")\
    .setLabel(u"Referencia Catastral")\
    .setShortLabel(u"Ref. catastral")\
    .setDescription(u"Identificador oficial y obligatorio de la parcela SIGPAC del recinto")
  add_TipoSuperficie(ft, "SupSIGPAC")\
    .setLabel(u"Superficie SIGPAC")\
    .setShortLabel(u"Sup. SIGPAC")\
    .setDescription(u"Superficie del recinto SIGPAC")
  add_TipoUsosSIGPAC(ft, "UsoSIGPAC")\
    .setLabel(u"Uso SIGPAC")\
    .setShortLabel(u"Uso SIGPAC")\
    .setDescription(u"Uso SIGPAC")
  add_TipoIndicadorSN(ft, "CtrComplRecNuevos")\
    .setLabel(u"Control complementario de recintos nuevos")\
    .setShortLabel(u"Control compl. recintos nuevos")\
    .setDescription(u"Marca para el control complementario de recintos nuevos")
  add_TipoCAPDeclarado(ft, "TipoCAPDeclarado")\
    .setLabel(u"CAP declarado")\
    .setShortLabel(u"CAP declarado")\
    .setDescription(u"CAP declarado: Prevalece al SIGPAC salvo lo modifique el agricultor")
  add_TipoSuperficie(ft, "SupNeta")\
    .setLabel(u"Superficie neta")\
    .setShortLabel(u"Sup. neta")\
    .setDescription(u"Superficie neta del recinto en areas.")
  add_TipoRegimenTenencia(ft, "RegTenencia")\
    .setLabel(u"Regimen tenencia")\
    .setShortLabel(u"Reg. tenencia")\
    .setDescription(u"Regimen de tenencia")
  add_TipoIndicadorSN(ft, "Extran_Arrendador")\
    .setLabel(u"Nº de identificacion corresponde a extranjero")\
    .setShortLabel(u"Nº idef. extrajero")\
    .setDescription(u"Numero de identificacion del arrendador si es extranjero")

  # discrepancia con el pdf
  # - Letra CIF arrendador
  # - DNI arrendador
  # - Letra NIF arrendador
  # en el xsd solo aparece un ID_arrendador
  add_TipoCIFNIFNIE(ft, "ID_arrendador")\
    .setLabel(u"ID arrendador")\
    .setShortLabel(u"ID arrendador")\
    .setDescription(u"ID arrendador")
  add_TipoIndicadorSN(ft, "CC_No_SIGPAC")\
    .setLabel(u"Concentracion parcelaria no integrada SIGPAC")\
    .setShortLabel(u"Conc. parc. no integrada SIGPAC")\
    .setDescription(u"Concentracion parcelaria no integrada en SIGPAC")
  add_TipoIndicadorSN(ft, "PastoComunal")\
    .setLabel(u"Pastro declarado en comun")\
    .setShortLabel(u"Pasto en comun")\
    .setDescription(u"Pasto en comun")
  add_TipoNombreRazonSocial90(ft, "NombrePasto")\
    .setLabel(u"Nombre del pasto")\
    .setShortLabel(u"Nombre pasto")\
    .setDescription(u"Nombre del pasto")
  add_TipoCodigoMUP(ft, "CodPasto")\
    .setLabel(u"Codigo del pasto")\
    .setShortLabel(u"Cod. pasto")\
    .setDescription(u"Codigo del pasto")
  add_TipoIndicadorSN(ft, "ZLN")\
    .setLabel(u"Zona con limitaciones naturales")\
    .setShortLabel(u"Zona lim. naturales")\
    .setDescription(u"Zona con limitaciones naturales")
  add_TipoIndicadorSN(ft, "AprovForrajero")\
    .setLabel(u"Recinto con aprovechamiento forrajero")\
    .setShortLabel(u"Aprov. forrajero")\
    .setDescription(u"Recinto con aprovechamiento forrajero")
  add_TipoObservaciones(ft, "Observaciones")\
    .setLabel(u"Observaciones")\
    .setShortLabel(u"Observaciones")\
    .setDescription(u"Observaciones")
  add_TipoIndicadorSN(ft, "SIE")\
    .setLabel(u"SIE")\
    .setShortLabel(u"SIE")\
    .setDescription(u"SIE")
  add_TipoRecuentoArboles(ft, "NumAlmendros")\
    .setLabel(u"Nº Almendros")\
    .setShortLabel(u"Nº Almendros")\
    .setDescription(u"Numero de arboles de almendros")
  add_TipoRecuentoArboles(ft, "NumAvellanos")\
    .setLabel(u"Nº Avellanos")\
    .setShortLabel(u"Nº Avellanos")\
    .setDescription(u"Numero de arboles de avellanos")
  add_TipoRecuentoArboles(ft, "NumAlgarrobos")\
    .setLabel(u"Nº Algarrobos")\
    .setShortLabel(u"Nº Algarrobos")\
    .setDescription(u"Numero de arboles de algarrobos")
  add_TipoRecuentoArboles(ft, "NumCastanos")\
    .setLabel(u"Nº Castanyos")\
    .setShortLabel(u"Nº Castanyos")\
    .setDescription(u"Numero de arboles de castanyos")
  add_TipoAnyo(ft, "AnoPlantFrutales")\
    .setLabel(u"Anyo plantacion (para frutales)")\
    .setShortLabel(u"Anyo plantacion (frutales)")\
    .setDescription(u"Anyo de plantacion. Formato AAAA")
  add_TipoSistCultivoHorticolas(ft, "SistCultivoHorticolas")\
    .setLabel(u"Sistema de cultivo")\
    .setShortLabel(u"Sis. cultivo")\
    .setDescription(u"Sistema de cultivo (para horticolas y flores)")
  add_TipoDestinoProduccion(ft, "Destino")\
    .setLabel(u"Destino de la produccion")\
    .setShortLabel(u"Dest. produccion")\
    .setDescription(u"Destino de la produccion (para cultivos proteicos, horticolas, energicos y florales")
  add_TipoNombreRazonSocial90(ft, "Nombre_AGPC")\
    .setLabel(u"Nombre o razon social")\
    .setShortLabel(u"Nombre o razon social")\
    .setDescription(u"")
  add_TipoIndicadorSN(ft, "Extran_AGPC")\
    .setLabel(u"Nº de identificacion corresponde a extranjero")\
    .setShortLabel(u"Nº ident. extranjero")\
    .setDescription(u"")
  # discrepancia con el pdf
  # - Letra CIF 
  # - DNI 
  # - Letra NIF
  # en el xsd solo aparece un ID_AGPC
  # TODO: label
  add_TipoCIFNIFNIE(ft, "ID_AGPC")\
    .setLabel(u"CIF (AGPC)")\
    .setShortLabel(u"CIF (AGPC)")\
    .setDescription(u"Datos de la autoridad Gestora del Pastro declarado en comun")
    
  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC/LD_Linea_AyudaSolAD
  add_relatedFeatures(ft, 
    "LD_Linea_AyudaSolAD", 
    "RSUPAC2019_RECINTOS_SIGPAC_AD", 
    "ID", 
    ("ID", "ID_RECINTO", "AyudaRecinto"), 
    "FEATURES('RSUPAC2019_RECINTOS_SIGPAC_AD',FORMAT('ID_RECINTO = ''%s''',ID_RECINTO))"
  )\
  .setGroup("Ayuda AD")

  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC/LD_Linea_AyudaSolPDR
  add_relatedFeatures(ft, 
    "LD_Linea_AyudaSolPDR", 
    "RSUPAC2019_RECINTOS_SIGPAC_PDR", 
    "ID", 
    ("ID", "ID_RECINTO", "LD_LineaSolicitadaPDR", "LD_SupSolicitadaPDR"), 
    "FEATURES('RSUPAC2019_RECINTOS_SIGPAC_AD',FORMAT('ID_RECINTO = ''%s''',ID_RECINTO))"
  )\
  .setGroup("Ayuda PDR")

  add_TipoProducto(ft, "ProductoCS")\
    .setLabel(u"Producto (CS)")\
    .setShortLabel(u"Producto (CS)")\
    .setDescription(u"Producto (CS)")\
    .getTags().set("dynform.separator","Cultivo Secundario")
  add_TipoVariedad(ft, "VariedadCS")\
    .setLabel(u"Variedad (CS)")\
    .setShortLabel(u"Variedad (CS)")\
    .setDescription(u"Variedad (CS)")
  add_TipoSemilla(ft, "TipSemillaCS")\
    .setLabel(u"Tipo de Semilla (CS)")\
    .setShortLabel(u"Tip. Semilla (CS)")\
    .setDescription(u"Tipo de Semilla (CS)")
  
  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC/CultivoSecundario/AyudaSecundario
  add_relatedFeatures(ft, 
    "AyudaSecundario", 
    "RSUPAC2019_RECINTOS_SIGPAC_AS", 
    "ID", 
    ("ID", "ID_RECINTO", "AyudaSolicitadaSecundario"), 
    "FEATURES('RSUPAC2019_RECINTOS_SIGPAC_AS',FORMAT('ID_RECINTO = ''%s''',ID_RECINTO))"
  )\
  .setGroup("Ayudas (CS)")

  add_TipoDestinoProduccion(ft, "DestinoCS")\
    .setLabel(u"Destino de la produccion (CS)")\
    .setShortLabel(u"Dest. produccion (CS)")\
    .setDescription(u"Destino de la produccion (para cultivos proteicos, horticolas, energeticos y flores)")
  
  # todo: ??? tag estoy fuera del CultivoSecundario
  
  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC/CultivosHorticolas
  add_relatedFeatures(ft, 
    "CultivosHorticolas", 
    "RSUPAC2019_RECINTOS_SIGPAC_AS", 
    "ID", 
    ("ID", "ID_RECINTO", "ProductoCH", "VariedadCH"), 
    "FEATURES('RSUPAC2019_RECINTOS_SIGPAC_AS',FORMAT('ID_RECINTO = ''%s''',ID_RECINTO))"
  )\
  .setGroup("Ayudas (CS)")

  add_TipoCoordenada(ft, "CoordX_Centroide")\
    .setLabel(u"Centroide: Coordenada X")\
    .setShortLabel(u"coord. X")\
    .setDescription(u"Centroide: Coordenada X")
  add_TipoCoordenada(ft, "CoordY_Centroide")\
    .setLabel(u"Centroide: Coordenada Y")\
    .setShortLabel(u"coord. Y")\
    .setDescription(u"Centroide: Coordenada Y")
    
  add_TipoRecintoCompleto(ft, "Completo")

  # TODO: Hay que recuperar el campo geometria
  """
  x = ft.add("GEOMETRY","Geometry")\
    .setGeometryType(Geometry.TYPES.MULTIPOLYGON, Geometry.SUBTYPES.GEOM2D)\
    .setSRS(u'EPSG:4326')\
    .setHidden(True)
  """
  
def add_fields_RSUPAC2019_RECINTOS_SIGPAC_CH(ft):
  ft.setLabel("RSU PAC 2019 - Cultivos horticolas")

  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC

  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  ft.add("ID_RECINTO", "Integer")\
    .setIsIndexed(True)\
    .setLabel("Recinto")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_R10_PARCELAS")\
    .set("foreingkey.code","ID_RECINTO")\
    .set("foreingKey.Label","FORMAT('%d %s %d %d',ID_RECINTO,RefCatastral, Completo,SupRecintoDec)")\
    .set("foreingkey.closedlist",False)
  
  add_TipoProducto(ft, "ProductoCH")\
    .setLabel(u"Producto (CH)")\
    .setShortLabel(u"Producto (CH)")\
    .setDescription(u"Producto (Cultivo horticola)")
  add_TipoVariedad(ft, "VariedadCH")\
    .setLabel(u"Variedad (CH)")\
    .setShortLabel(u"Variedad (CH)")\
    .setDescription(u"Variedad (Cultivo horticola)")
  
def add_fields_RSUPAC2019_RECINTOS_SIGPAC_AS(ft):
  ft.setLabel("RSU PAC 2019 - Ayudas solicitadas secundarias")

  # RSU/Parcelas/R10_Parcelas/LD_RecintoSIGPAC
  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  ft.add("ID_RECINTO", "Integer")\
    .setIsIndexed(True)\
    .setLabel("Recinto")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_R10_PARCELAS")\
    .set("foreingkey.code","ID_RECINTO")\
    .set("foreingKey.Label","FORMAT('%d %s %d %d',ID_RECINTO,RefCatastral, Completo,SupRecintoDec)")\
    .set("foreingkey.closedlist",False)
  
  #campo 55
  add_TipoLineaADSecundario(ft, "AyudaSolicitadaSecundario")\
    .setLabel(u"Ayuda solicitada (secundaria)")\
    .setShortLabel(u"Ayuda solicitada (secundaria)")\
    .setDescription(u"Ayuda solicitada del cultivo secundario")

def add_fields_RSUPAC2019_RECINTOS_SIGPAC_PDR(ft):
  ft.setLabel("RSU PAC 2019 - Ayudas recinto PDR")

  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  ft.add("ID_RECINTO", "Integer")\
    .setIsIndexed(True)\
    .setLabel("Recinto")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_R10_PARCELAS")\
    .set("foreingkey.code","ID_RECINTO")\
    .set("foreingKey.Label","FORMAT('%d %s %d %d',ID_RECINTO,RefCatastral, Completo,SupRecintoDec)")\
    .set("foreingkey.closedlist",False)

  #campo 50
  add_TipoLineaPDR(ft, "LD_LineaSolicitadaPDR")\
    .setLabel(u"Codigo de la Linea de ayuda solicitada")\
    .setShortLabel(u"Cod. ayuda")\
    .setDescription(u"Codigo de la Linea de ayuda solicitada PDR por recinto multi-registro")
  #campo 51
  add_TipoSuperficie(ft, "LD_SupSolicitadaPDR")\
    .setLabel(u"Superficie solicitada por linea de ayuda")\
    .setShortLabel(u"Sup. ayuda")\
    .setDescription(u"Superficie solicitada por linea de ayuda PDR multi-registro")

def add_fields_RSUPAC2019_RECINTOS_SIGPAC_AD(ft):
  ft.setLabel("RSU PAC 2019 - Ayudas recinto AD")

  ft.add("ID", "Integer")\
    .setIsPrimaryKey(True)
  ft.add("ID_RECINTO", "Integer")\
    .setIsIndexed(True)\
    .setLabel("Recinto")\
    .setAllowNull(False)\
    .set("foreingkey",True)\
    .set("foreingkey.table","RSUPAC2019_R10_PARCELAS")\
    .set("foreingkey.code","ID_RECINTO")\
    .set("foreingKey.Label","FORMAT('%d %s %d %d',ID_RECINTO,RefCatastral, Completo,SupRecintoDec)")\
    .set("foreingkey.closedlist",False)
        
  #campo 49
  add_TipoLineaAD(ft, "AyudaRecinto")\
    .setLabel(u"Ayuda solicitada")\
    .setShortLabel(u"Ayuda solicitada")\
    .setDescription(u"Ayuda solicitada")

def main(*args):
  pass
  