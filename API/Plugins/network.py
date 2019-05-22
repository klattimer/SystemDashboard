import cherrypy
import psutil
from API import APIPluginInterface
import logging

__plugin__ = "NetworkAPI"
__plugin_version__ = "0.1"


class NetworkAPI(APIPluginInterface):
    api_path = "/api/network"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    scripts = [
        {
            "src": "Javascript/network.js"
        }
    ]

    menuitems = [{
        "id": "network",
        "icon": "fas fa-network-wired",
        "name": "Network",
        "order": 3
    }]
    widgets = {
        "traffic": {
            "type": "LineChart",
            "size": "w2h1",
            "id": "traffic",
            "fa_icon": "far ",
            "title_label": "Network Traffic",
            "menuitem": "network"
        }
    }
    templates = [
        "LineChart"
    ]

    def __init__(self, server):
        super(NetworkAPI, self).__init__(server)

    def GET(self, **params):
        psutil.net_io_counters(pernic=True)
        return {
            "addresses": psutil.net_if_addrs(),
            "io": psutil.net_io_counters(pernic=True, nowrap=True),
            "stats": psutil.net_if_stats(),
            "radar_data": []
        }
