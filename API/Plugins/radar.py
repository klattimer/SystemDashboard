import cherrypy
import psutil
from API import APIPluginInterface
from Common.tools import get_primary_ip
from Common.ping import ping
import logging
import netaddr

__plugin__ = "RadarAPI"
__plugin_version__ = "0.1"


class RadarAPI(APIPluginInterface):
    api_path = "/api/network"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
        }
    }

    def __init__(self, server):
        super(RadarAPI, self).__init__(server)

    def GET(self, **params):
        addresses = psutil.net_if_addrs()
        ip = get_primary_ip()
        for device in addresses.keys():
            for address in addresses[device]:
                if address.address == ip:
                    netmask = address.netmask

        network = ip + '/' + str(IPAddress(netmask).netmask_bits())
        address_list = list(netaddr.IPNetwork(network).iter_hosts())
        for address in address_list:
            print (address)