import cherrypy
import psutil
from API import APIPluginInterface
from Common.tools import get_primary_ip
from Common.ping import ping
import logging
import netaddr
from multiprocessing.pool import ThreadPool
from time import sleep


__plugin__ = "RadarAPI"
__plugin_version__ = "0.1"


def lping(address, timeout):
    delay = ping(str(address), timeout=0.5)
    return (address, delay)

class RadarAPI(APIPluginInterface):
    api_path = "/api/radar"
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

        network = ip + '/' + str(netaddr.IPAddress(netmask).netmask_bits())
        address_list = list(netaddr.IPNetwork(network).iter_hosts())
        ping_results = []

        pool = ThreadPool(processes=1000)
        async_results = []
        for address in address_list:
            logging.debug("Pinging " + str(address))
            async_results.append(pool.apply_async(lping, (str(address), 0.5)))

        sleep(1)

        for asyng_result in async_results:
                ping_results.append(asyng_result.get())

        return [ping for ping in ping_results if ping[1] > 0]
