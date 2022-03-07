"""
SNMPv1
++++++
Send SNMP GET request using the following options:
  * with SNMPv1, community 'comunidadASR'
  * over IPv4/UDP
  * to an Agent at localhost
  * for two instances of SNMPv2-MIB::sysDescr.0 MIB object,
Functionally similar to:
| $ snmpget -v1 -c comunidadASR localhost 1.3.6.1.2.1.1.1.0
"""#
from pysnmp.hlapi import *
def Consulta(hostname,version,comunidad,puerto,oid):
    version-=1
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(comunidad, mpModel=version),
        UdpTransportTarget((hostname, puerto)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)
        return False

    elif errorStatus:
        
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        return False
    else:
        for varBind in varBinds:
            resultado = ' = '.join([x.prettyPrint() for x in varBind])
            return resultado



def getSystem(hostname,version,comunidad,puerto):
    descripcion = Consulta(hostname,version,comunidad,puerto)
    descripcion = descripcion.split(' ')
    if('Windows' in descripcion):
        return 'Windows'
    elif('Linux' in descripcion):
        return 'Linux'
    else:
        return 'Desconocido'