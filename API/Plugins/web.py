import cherrypy
from API import APIPluginInterface, WidgetLookup
import logging
import os
from copy import copy
from collections import namedtuple
import json

__plugin__ = "WebAPI"
__plugin_version__ = "0.1"

def frozenDict(d):
    fd = namedtuple('FrozenDict', sorted(d.keys()))
    return fd(**d)


class WebAPI(APIPluginInterface):
    api_path = "/"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.Dispatcher(),
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Static")),
            'tools.jwtauth.on': True,
            'tools.jwtauth.required': False
        }
    }
    scripts = [
        {
            "src": "http://code.jquery.com/jquery-3.3.1.min.js",
            "integrity": "sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=",
            "crossorigin": "anonymous",
        },
        {
            "src": "https://code.jquery.com/ui/1.12.1/jquery-ui.min.js",
            "integrity": "sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=",
            "crossorigin": "anonymous",
        },
        {
            "src": "https://cdn.jsdelivr.net/npm/chart.js@2.8.0/dist/Chart.min.js",
            "integrity": "sha256-Uv9BNBucvCPipKQ2NS9wYpJmi8DTOEfTA/nH2aoJALw=",
            "crossorigin": "anonymous",
        },
        {
            "src": "https://unpkg.com/masonry-layout@4/dist/masonry.pkgd.min.js",
            "crossorigin": "anonymous",
        },
        {
            "src": "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment-with-locales.min.js",
            "crossorigin": "anonymous",
        },
        {
            "src": "https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.1.2/handlebars.js",
            "crossorigin": "anonymous",
        },
        {
            "src": "Javascript/main.js"
        },
        {
            "src": "Javascript/scrolltoname.js"
        }
    ]
    styles = [
        {
             "rel": "stylesheet",
             "href": "https://use.fontawesome.com/releases/v5.8.0/css/all.css",
             "integrity": "sha384-Mmxa0mLqhmOeaE8vgOSbKacftZcsNYDjQzuCOm6D02luYSzBG8vpaOykv9lFQ51Y",
             "crossorigin": "anonymous"
        },
        {
            "href": "https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i",
            "rel": "stylesheet"
        },
        {
            "rel": "stylesheet",
            "type": "text/css",
            "href": "CSS/main.css"
        },
        {
            "rel": "stylesheet",
            "type": "text/css",
            "href": "CSS/widget-grid.css"
        },
        {
            "rel": "stylesheet",
            "type": "text/css",
            "href": "CSS/tables.css"
        }
    ]

    def __init__(self, server):
        super(WebAPI, self).__init__(server)
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Templates"))
        #self.lookup = TemplateLookup(directories=[path])
        self.lookup = WidgetLookup(directories=[path])

    def collect(self):
        theme = {
            "href": "CSS/theme-%s.css" % self._server.conf['theme'],
            "type": "text/css",
            "rel": "stylesheet"
        }
        styles = [frozenDict(theme)]
        styles += [frozenDict(s) for s in self.__class__.styles]
        scripts = [frozenDict(s) for s in self.__class__.scripts]
        templates = set()
        menuitems = []
        widgets = []

        for plugin in self._server.api.plugins:
            if plugin == self: continue
            scripts += [frozenDict(s) for s in plugin.__class__.scripts]
            styles += [frozenDict(s) for s in plugin.__class__.styles]
            templates.update(set(plugin.__class__.templates))
            menuitems += [frozenDict(m) for m in plugin.__class__.menuitems]
            widgets += [plugin.__class__.widgets]

        # Remove duplicate scripts & styles, that's why these were loaded as a frozenDict
        # we need them to be hashable
        print (scripts)
        print (styles)
        scripts = sorted(set(scripts),key=scripts.index)
        styles = sorted(set(styles),key=styles.index)
        templates = list(set(templates))
        print()
        print(menuitems)
        print()
        menuitems = list(set(menuitems))

        print(menuitems)
        print()
        menuitem_id_list = list(set([menuitem.id for menuitem in menuitems]))
        menuitems = [m._asdict() for m in menuitems]
        menuitems.sort(key=lambda x: x['order'])
        print(menuitems)
        print()

        w = {}
        for widgetgroup in widgets:
            for widget_key, widget in widgetgroup.items():
                if widget['type'] not in templates:
                    raise cherrypy.HTTPError(403, "Missing template" + widget['type'])
                print (widget)
                if widget['menuitem'] not in menuitem_id_list:
                    raise cherrypy.HTTPError(403, "Missing menuitem" + widget['menuitem'])
                if widget_key in w.keys():
                    raise cherrypy.HTTPError(403, "Duplicate widget key " + widget_key)
                w[widget_key] = widget

        return (scripts, styles, templates, menuitems, w)

    def generate_scripts(self, scripts):
        tags = []
        for script in scripts:
            script = script._asdict()
            attributes = ["%s=\"%s\"" % (k,v) for (k,v) in script.items()]
            tag = '<script ' + ' '.join(attributes) + '></script>';
            tags.append(tag)
        return ''.join(tags)

    def generate_styles(self, styles):
        tags = []
        for style in styles:
            style = style._asdict()
            attributes = ["%s=\"%s\"" % (k,v) for (k,v) in style.items()]
            tag = '<link ' + ' '.join(attributes) + ' />';
            tags.append(tag)
        return ''.join(tags)

    def generate_templates(self, templates):
        tags = []
        for template in templates:
            t = self.lookup.get_template(template)
            tags.append(t.render())
        return ''.join(tags)

    def generate_pagedata(self, pagedata):
        return "<script id=\"page-data\" type=\"application/json\">%s</script>" % json.dumps(pagedata)

    @cherrypy.expose
    def index(self):
        (scripts, styles, templates, menuitems, widgets) = self.collect()
        style_tags = self.generate_styles(styles)
        script_tags = self.generate_scripts(scripts)
        template_tags = self.generate_templates(templates)
        page_data = self.generate_pagedata({'widgets': widgets})

        output = self.lookup.get_template("container.html")
        head = style_tags + script_tags + template_tags + page_data
        return output.render(head=head, menuitems=menuitems)
