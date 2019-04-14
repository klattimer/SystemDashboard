import cherrypy
import psutil
from API import APIPluginInterface
import subprocess
import logging
import mdstat
import json

__plugin__ = "DiskAPI"
__plugin_version__ = "0.1"


class DiskAPI(APIPluginInterface):
    api_path = "/api/disk"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    def __init__(self, server):
        super(DiskAPI, self).__init__(server)

    def get_hdd_temp(self, hdd):
        try:
            for line in subprocess.Popen([b'sudo', b'smartctl', b'-a', bytes('/dev/' + hdd, encoding='utf8')], stdout=subprocess.PIPE).stdout.read().split(b'\n'):
                if ( b'Temperature_Celsius' in line.split() ) or (b'Temperature_Internal' in line.split() ):
                    return int(line.split()[9])
        except:
            logging.exception("Couldn't get disk temperature")

    def GET(self, **params):
        partitions = psutil.disk_partitions(all=False)
        diskusage = {}
        disks = []
        for partition in partitions:
            if 'loop' in partition.device: continue
            diskusage[partition.mountpoint] = psutil.disk_usage(partition.mountpoint)
            if 'md' in partition.device: continue
            disk = partition.device.replace('/dev/', '')
            disk = ''.join(i for i in disk if not i.isdigit())
            disks.append(disk)

        try:
            md = mdstat.parse()
            for array in md['devices'].keys():
                for disk in md['devices'][array]['disks'].keys():
                    disks.append(''.join(i for i in disk if not i.isdigit()))
        except:
            md = {}

        disks = list(set(disks))
        disks.sort()
        temperatures = {'/dev/' + k: self.get_hdd_temp(k) for k in disks}


        return {
            "partitions": partitions,
            "usage": diskusage,
            "temperatures": temperatures,
            'mdstat': md,
            'disks': disks
        }
