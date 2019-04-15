import importlib
import os
import logging
import cherrypy


class APIPluginInterface(object):
    exposed = True
    api_path = None
    api_config = {}
    scripts = []
    styles = []

    def __init__(self, server):
        self._server = server
        super(APIPluginInterface, self).__init__()


class APIRegistry(object):
    def __init__(self, server):
        self.__server = server
        files = os.listdir(os.path.join(os.path.dirname(__file__), "Plugins"))
        for f in files:
            if f.startswith('__'): continue

            module_name = __name__ + ".Plugins." + f[:-3]
            try:
                module = importlib.import_module(module_name)
                plugin = getattr(module, str(module.__plugin__))
                logging.info("Loaded plugin named " + module_name)
            except:
                logging.exception("Cannot load plugin named " + module_name)
                continue
            self.register(plugin(server))

    def register(self, plugin):
        cherrypy.tree.mount(plugin, plugin.__class__.api_path, plugin.__class__.api_config)
        logging.info("Mounting plugin " + plugin.__class__.__name__ + " on " + plugin.__class__.api_path)
