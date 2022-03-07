import os
from time import sleep
import time
from SNMPget import *
from RRDcreator import *
import threading
from Reporte import *
from Agente import *

#oids
NUMERO_DE_INTERFACES = '1.3.6.1.2.1.2.1.0'
INFORMACION_INTERFAZ = '1.3.6.1.2.1.2.2.1.2.'
ESTADO_INTERFAZ = '1.3.6.1.2.1.2.2.1.7.'

class Menu:

    def Operacion(opcion,hosts):
        if(opcion == 1):
            print('Agregando agente')
            hostname = input('Introduzca el hostname del agente: ')
            version = int(input('Introduzca la version SNMP: '))
            comunidad = input('Introduce la comunidad: ')
            puerto = int(input('Introduce el puerto: '))
            a = Agente(hostname,version,comunidad,puerto)
            a.addAgente()
            Menu()
        elif(opcion==2):
            print('Eliminando agente')
            hostname = input('Introduce el hostname del agente: ')
            Agente.deleteAgente(hostname)
            sleep(3)
            Menu()
        elif(opcion==3):
            print('Crear Reporte')
            print('Agentes registrados:')
            for i in hosts:
                print('-',i[0])
            hostname = input('Introduce el hostname del agente:')
            hostname = Agente.getAgente(hostname)
            T = str(int(time.time()) - 600)
            RRDcreator.graph(hostname[0],'inmulticast','Paquetes multicast recibidos', 'Paquetes', T, 'N')
            RRDcreator.graph(hostname[0], 'inip', 'Paquetes recibidos con ex al protocolo ipv4', 'Paquetes', T, 'N')
            RRDcreator.graph(hostname[0], 'icmpecho', 'Mensajes ICMP de respuesta', 'Mensajes', T, 'N')
            RRDcreator.graph(hostname[0], 'tcpsegsin', 'Segmentos TCP enviados', 'Segmentos', T, 'N')
            RRDcreator.graph(hostname[0], 'udpindtgr', 'Datagramas recibidos que no fueron entregados', 'Datagramas', T, 'N')
            r = Reporte(hostname)
            r.CrearReporte()
            print('Reporte elaborado con exito')
            Menu()
        elif(opcion==4):
            quit()
        else:
            print('Esa opcion no existe, escoja otra valida')
            Menu()

    def Opciones(hosts):
        print('Operaciones disponibles')
        print('1-Agregar agente')
        print('2-Eliminar agente')
        print('3-Realizar reporte de un agente')
        print('4-Salir')
        opcion = int(input("Escoja una opcion: "))
        Menu.Operacion(opcion,hosts)

    def __init__(self):
        self.host_disponibles = []
        agentes = Agente.getAgentes()
        print('Resumen')
        print('Host registrados:',len(agentes))
        if(len(agentes)!=0):
            for i in agentes:
                numero_interfaces = consulta(i[0],i[1],i[2],i[3],NUMERO_DE_INTERFACES)
                estado = 'up' if numero_interfaces != False else 'down'
                print('Hostname del agente:',i[0])
                if(numero_interfaces == False):
                    numero_interfaces = 'down'
                    print('Cantidad de Interfaces:',numero_interfaces)
                    print('Status del Agente:',estado)
                else:
                    print('Cantidad de Interfaces:',numero_interfaces)
                    print('Status del Agente:',estado)
                    self.host_disponibles.append(i)
                    print('Lista de Interfaces')
                    for interfaz in range(1,int(numero_interfaces)+1):

                        descripcion = str(consulta(i[0],i[1],i[2],i[3],INFORMACION_INTERFAZ+str(interfaz)))
                        interfaz_estado = int(consulta(i[0],i[1],i[2],i[3],ESTADO_INTERFAZ+str(interfaz)))
                        descripcion = getDescription(descripcion)
                        interfaz_estado = 'up' if interfaz_estado == 1 else 'down'
                        print('Numero:',interfaz,descripcion,'- Status:',interfaz_estado)
        else:
            print('No existe ningun agente registrado')
        print(self.host_disponibles)
        m = RRDcreator(self.host_disponibles)
        m.CrearCarpetas()
        m.CrearRRD()
        hilo = threading.Thread(target=m.Update,)
        hilo2 = threading.Thread(target=Menu.Opciones,args=(self.host_disponibles,),)
        hilo.start()
        hilo2.start()

if(__name__ == '__main__'):
    Menu()