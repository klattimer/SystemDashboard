from mako.template import Template
from mako.lookup import TemplateLookup
from mako.lookup import TemplateCollection
import glob
import logging
import os



class WidgetLookup(TemplateCollection):
    def __init__(self, directories):
        # Locate all .mako files in the path, if the file is called template.mako
        # then take the directory name as the template lookup uri
        self.__templates = {}
        for path in directories:
            path = os.path.abspath(path)
            logging.debug("Checking path " + path)
            templates = glob.glob(path + '/**', recursive=True)
            for f in templates:
                if os.path.isdir(f): continue
                p = f.split('/')
                if p[-1] == 'template.mako':
                    self.__templates[p[-2]] = f
                    logging.debug("adding " + p[-2])
                else:
                    self.__templates[p[-1]] = f
                    logging.debug("adding " + p[-1])

    def has_template(self, uri):
        if uri in self.__templates.keys(): return True
        return False

    def get_template(self, uri, relativeto=None):
        print (self.__templates.keys())
        template_path = self.__templates[uri]
        return Template(filename=template_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    menuitems = [{
        "id": "storage",
        "icon": "far fa-hdd",
        "name": "Storage",
        "order": 2,
    }]
    menuitems.append({
        "id": "load",
        "icon": "fas fa-weight-hanging",
        "name": "System Load",
        "order": 1
    })
    menuitems.append({
        "id": "users",
        "icon": "fas fa-users",
        "name": "Users",
        "order": 3
    })

    mylookup = WidgetLookup(directories=[os.path.dirname(os.path.abspath(__file__))])
    t = mylookup.get_template('MenuItem')
    mytemplate = Template(filename='makotest.html', lookup=mylookup)
    print(mytemplate.render(**{'menuitems': menuitems}))
