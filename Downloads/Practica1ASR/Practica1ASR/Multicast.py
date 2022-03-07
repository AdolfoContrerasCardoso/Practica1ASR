from SNMPget import *

#OIDS
PACKET_MULTICAST_INT = '1.3.6.1.2.1.2.2.1.12.'
NUMERO_DE_INTERFACES = '1.3.6.1.2.1.2.1.0'
GET_SYSTEM = '1.3.6.1.2.1.1.1.0'

def getOidMulticast(localhost,version,comunidad,puerto):
    oids = []
    num_de_interfaces =  int(consulta(localhost,version,comunidad,puerto,NUMERO_DE_INTERFACES))
    for i in range(1,num_de_interfaces+1):
        counter = int(consulta(localhost,version,comunidad,puerto,PACKET_MULTICAST_INT+str(i)))
        if(counter!= 0):
            print('Numero de interfaz:',i,'- Valor:',counter)
            oid = f'{PACKET_MULTICAST_INT}{i}'
            oid = str(oid)
            oids.append(oid)
        else:
            pass
    if(len(oids)==0):
        oids[0] = False
    
    return oids[0]

def getSystem(localhost,version,comunidad,puerto):
    get_system =  (consulta(localhost,version,comunidad,puerto,GET_SYSTEM))
    get_system = get_system.split(' ')
    if('Linux' in get_system):
        return 'Linux'
    else:
        return 'Windows'
