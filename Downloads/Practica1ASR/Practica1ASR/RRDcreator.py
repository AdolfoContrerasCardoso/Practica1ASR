from os import *
import rrdtool
from SNMPget3 import *

OIDS = [
    '1.3.6.1.2.1.2.2.1.12.1',
    '1.3.6.1.2.1.4.9.0',
    '1.3.6.1.2.1.5.22.0',
    '1.3.6.1.2.1.6.11.0',
    '1.3.6.1.2.1.7.3.0'

]

class RRDcreator():

    def create(host):
        ret = rrdtool.create(f'{host}/{host}.rrd',
                            "--start",'N',
                            "--step",'60',
                            "DS:inmulticast:COUNTER:600:U:U",
                            "DS:inip:COUNTER:600:U:U",
                            "DS:icmpecho:COUNTER:600:U:U",
                            "DS:tcpsegsin:COUNTER:600:U:U",
                            "DS:udpindtgr:COUNTER:600:U:U",
                            "RRA:AVERAGE:0.5:6:5",
                            "RRA:AVERAGE:0.5:1:30")
        if ret:
            print (rrdtool.error())

    def Update(self):
        while(True):
            for host in self.host:
                info = [getConsulta(host[0],host[1],host[2],host[3],oid) for oid in OIDS]
                info = 'N:' + ':'.join([str(e) for e in info])
                rrdtool.update(f'{host[0]}/{host[0]}.rrd', info)
                rrdtool.dump(f'{host[0]}/{host[0]}.rrd', f'{host[0]}/{host[0]}.xml')

    def graph(host, var, title, descr, t0 = 'N', tf = 'N'):
        ret = rrdtool.graph(f'{host}/{host} {var}.png',
                        "--start",t0,
                        "--end",tf,
                        "--vertical-label=Bytes/s",
                        f"--title={title}",
                        f"DEF:{var}={host}/{host}.rrd:{var}:AVERAGE",
                        f"LINE3:{var}#0000FF:{descr}") 


    def __init__(self,host):
        self.host = host
    
    def EliminarCarpeta(self):
        for i in self.host:
            rmdir(i[0])

    def CrearRRD(self):
        for i in self.host:
            RRDcreator.create(i[0])

    def CrearCarpetas(self):
        for i in self.host:
            makedirs(i[0],exist_ok=True)



