import importlib
import os
import logging
import cherrypy
from mako.template import Template
from mako.lookup import TemplateCollection
import glob

class WidgetLookup(TemplateCollection):
    def __init__(self, directories):
        # Locate all .mako files in the path, if the file is called template.mako
        # then take the directory name as the template lookup uri
        self.__templates = {}
        for path in directories:
            templates = glob.glob(path, recursive=True)
            for f in templates:
                p = f.split('/')
                if p[-1] == 'template.mako':
                    self.__templates[p[-2]] = f
                else:
                    self.__templates[p[-1]] = f

    def has_template(self, uri):
        if uri in self.__templates.keys(): return True
        return False

    def get_template(self, uri, relativeto=None):
        template_path = self.__templates[uri]
        return Template(filename=template_path)


class APIPluginInterface(object):
    exposed = True
    api_path = None
    api_config = {}
    scripts = []
    styles = []
    templates = []

    def __init__(self, server):
        self._server = server
        super(APIPluginInterface, self).__init__()


class APIRegistry(object):
    def __init__(self, server):
        self.__server = server
        files = os.listdir(os.path.join(os.path.dirname(__file__), "Plugins"))
        self.plugins = []
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
        self.plugins.append(plugin)
        cherrypy.tree.mount(plugin, plugin.__class__.api_path, plugin.__class__.api_config)
        logging.info("Mounting plugin " + plugin.__class__.__name__ + " on " + plugin.__class__.api_path)
