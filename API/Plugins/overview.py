import cherrypy
from API import APIPluginInterface
import logging
from datetime import timedelta
import platform
import os
import multiprocessing
from Common.tools import get_primary_ip

__plugin__ = "OverviewAPI"
__plugin_version__ = "0.1"


class OverviewAPI(APIPluginInterface):
    api_path = "/api/overview"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }
    scripts = [
        {
            "src": "Javascript/overview.js"
        }
    ]
    widgets = {
        "overview": {
            "type": "Overview",
            "size": "w4h1",
            "id": "overview",
            "fa_icon": ""
        }
    }
    templates = [
        "Overview"
    ]

    def __init__(self, server):
        super(OverviewAPI, self).__init__(server)

    def _get_platform(self):
        """
        Get the OS name, hostname and kernel
        """
        try:
            osname = " ".join(platform.linux_distribution())
            uname = platform.uname()

            if osname == '  ':
                osname = uname[0]

            data = {'osname': osname, 'hostname': uname[1], 'kernel': uname[2]}

        except Exception as err:
            data = str(err)

        return data

    def _get_cpus(self):
        """
        Get the number of CPUs and model/type
        """
        try:
            pipe = os.popen("cat /proc/cpuinfo | grep 'model name'")
            data = pipe.read().strip().split(':')[-1]
            pipe.close()

            if not data:
                pipe = os.popen("cat /proc/cpuinfo | grep 'Processor'")
                data = pipe.read().strip().split(':')[-1]
                pipe.close()

            cpus = multiprocessing.cpu_count()

            data = {'cpus': cpus, 'type': data}

        except Exception as err:
            data = str(err)

        return data


    def _get_uptime(self):
        '''
        Get uptime
        '''
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime_time = str(timedelta(seconds=uptime_seconds))
                data = uptime_time.split('.', 1)[0]

        except:
            logging.exception("Cannot get uptime")
            return

        return data

    def GET(self, **params):
        data = {}
        data['primary_ip'] = get_primary_ip()
        data['uptime'] = self._get_uptime()
        data['cpus'] = self._get_cpus()
        data.update(self._get_platform())

        return data
