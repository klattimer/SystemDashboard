import cherrypy
import psutil
from API import APIPluginInterface
import subprocess
import logging
import mdstat
import json

__plugin__ = "DiskIOAPI"
__plugin_version__ = "0.1"


class DiskIOAPI(APIPluginInterface):
    api_path = "/api/diskio"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    def __init__(self, server):
        super(DiskIOAPI, self).__init__(server)

    def resolve_partition(self, partition):
        device = p.device.replace('/dev/', '')
        if device == 'root':
            with open('/proc/cmdline') as cmdline:
                cmdline_text = cmdline.read()

            cmdline_args = {}
            for arg in cmdline_text.split(' '):
                try:
                    (k, v) = arg.split('=')
                except:
                    pass
                cmdline_args[k] = v
            device = cmdline_args['root']
            device.replace('/dev/', '')
        return device

    def GET(self, **params):
        partitions = psutil.disk_partitions(all=False)
        diskrw = psutil.disk_io_counters(perdisk=True)

        diskrw_data = {
            "read_bytes": 0,
            "write_bytes": 0,
        }

        io_disks = [self.resolve_partition(p) for p in partitions if 'loop' not in p.device]

        diskrw = {k: diskrw[k] for k in io_disks}
        for k in io_disks:
            diskrw_data['read_bytes'] += diskrw[k].read_bytes
            diskrw_data['write_bytes'] += diskrw[k].write_bytes

        return {
            "io": diskrw,
            "total_io": diskrw_data
        }
