from pysnmp.hlapi import *

def getConsulta(hostname,version,comunidad,puerto,oid):
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
	            return varBind[1]
