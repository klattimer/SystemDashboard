import cherrypy
import psutil
from API import APIPluginInterface
import logging

__plugin__ = "TopAPI"
__plugin_version__ = "0.1"


class TopAPI(APIPluginInterface):
    api_path = "/api/top"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }
    scripts = [
        {
            "src": "Javascript/top.js"
        }
    ]

    def __init__(self, server):
        super(TopAPI, self).__init__(server)

    def _list_processes(self):
        procs = []
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict()
                pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
                procs.append(pinfo)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return procs

    def GET(self, **params):
        errors = []
        try:
            procs = self._list_processes()
        except:
            logging.exception("Cannot get psutil data")
            self.errors.append({"type": "critical", "message": "psutil exception"})

        cpu = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:20]
        mem = sorted(procs, key=lambda p: p['memory_percent'], reverse=True)[:20]

        return {
            'top_cpu_usage': cpu,
            'top_memory_usage': mem,
            "errors": errors
        }
