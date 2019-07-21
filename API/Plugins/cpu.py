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

    menuitems = [{
        "id": "load",
        "icon": "fas fa-weight-hanging",
        "name": "System Load",
        "order": 2
    }]

    scripts = [
        {
            "src": "Javascript/cpu.js"
        },
        {
            "src": "Javascript/memory.js"
        }
    ]

    widgets = {
        "cpu": {
            "type": "LineChart",
            "size": "w2h1",
            "id": "cpu",
            "fa_icon": "fas fa-microchip",
            "title_label": "CPU History",
            "menuitem": "load"
        },
        "memory": {
            "type": "LineChart",
            "size": "w2h1",
            "id": "memory",
            "fa_icon": "fas fa-memory",
            "title_label": "Memory History",
            "menuitem": "load"
        },
        "loadave": {
            "type": "LineChart",
            "size": "w1h1",
            "id": "loadave",
            "fa_icon": "fas fa-bolt",
            "title_label": "Load Average",
            "menuitem": "load"
        },
        "sensors": {
            "type": "Table",
            "size": "w1h1",
            "id": "sensors",
            "fa_icon": "fas fa-thermometer-quarter",
            "headers": [
                { "title": "Device"},
                { "title": "Temperature"},
                { "title": "", "class": "narrow" }
            ],
            "title_label": "Thermal Sensors",
            "menuitem": "load"
        },
        "fans": {
            "type": "Table",
            "size": "w1h1",
            "id": "fans",
            "fa_icon": "fas fa-wind",
            "headers": [
                { "title": "Device"},
                { "title": "Speed"},
                { "title": "", "class": "narrow" }
            ],
            "title_label": "Fans",
            "menuitem": "load"
        }
    }

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
            logging.warning("Cannot get temperatures")
            data['errors'].append({"type": "warning", "message": "cannot get temperatures"})

        try:
            t = psutil.sensors_fans()
            for k in t.keys():
                for i, x in enumerate(t[k]):
                    t[k][i] = dict(x._asdict())
            data['fans'] = t
        except:
            logging.warning("Cannot get fan speeds")
            data['errors'].append({"type": "warning", "message": "cannot get fan speeds"})

        return data
