import cherrypy
import psutil
from API import APIPluginInterface
import logging

__plugin__ = "CPUAPI"
__plugin_version__ = "0.1"


class CPUAPI(APIPluginInterface):
    api_path = "/api/cpu"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    scripts = [
        {
            "src": "Javascript/load.js"
        },
        {
            "src": "Javascript/cpu.js"
        },
        {
            "src": "Javascript/memory.js"
        }
    ]

    def __init__(self, server):
        super(CPUAPI, self).__init__(server)

    def GET(self, **params):
        try:
            data = {
                "cpu_percent": psutil.cpu_percent(interval=1, percpu=True),
                "cpu_frequency": [i._asdict() for i in psutil.cpu_freq(percpu=True)],
                "memory": psutil.virtual_memory()._asdict(),
                "swap": psutil.swap_memory()._asdict(),
                "errors": []
            }
        except:
            logging.exception("Cannot get psutil data")
            data = {
                "cpu_percent": [],
                "cpu_frequency": [],
                "memory": {},
                "swap": {},
                "errors": [
                    {
                        "type": "critical",
                        "message": "psutil exception"
                    }
                ]
            }

        try:
            t = psutil.sensors_temperatures()
            for k in t.keys():
                for i, x in enumerate(t[k]):
                    t[k][i] = dict(x._asdict())
            data['temperatures'] = t
        except:
            logging.exception("Cannot get temperatures")
            data['errors'].append({"type": "warning", "message": "cannot get temperatures"})

        try:
            t = psutil.sensors_fans()
            for k in t.keys():
                for i, x in enumerate(t[k]):
                    t[k][i] = dict(x._asdict())
            data['fans'] = t
        except:
            logging.exception("Cannot get fan speeds")
            data['errors'].append({"type": "warning", "message": "cannot get fan speeds"})

        return data
