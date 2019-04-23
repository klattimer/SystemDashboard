import cherrypy
from API import APIPluginInterface
import logging

__plugin__ = "WebAPI"
__plugin_version__ = "0.1"


class WebAPI(APIPluginInterface):
    api_path = "/newroot"
    api_config = {
        '/': {
            'request.dispatch': cherrypy.dispatch.Dispatcher(),
            'tools.json_in.on': True,
            'tools.json_out.on': True
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

    def collect(self):
        scripts = []
        styles = []
        for plugin in self._server.api.plugins:
            scripts += plugin.__class__.scripts
            styles += plugin.__class__.styles
        return (scripts, styles)

    def generate_scripts(self, scripts):
        tags = []
        for script in scripts:
            attributes = ["%s=\"%s\"" % (k,v) for (k,v) in script.items()]
            tag = '<script ' + ' '.join(attributes) + '></script>';
            tags.append(tag)
        return ''.join(tags)

    def generate_styles(self, styles):
        tags = []
        for style in styles:
            attributes = ["%s=\"%s\"" % (k,v) for (k,v) in style.items()]
            tag = '<link ' + ' '.join(attributes) + ' />';
            tags.append(tag)
        return ''.join(tags)

    def index(self):
        (scripts, styles) = self.collect()
        style_tags = self.generate_styles(styles)
        script_tags = self.generate_scripts(scripts)
        return style_tags + '\n\n' + script_tags

    def signin(self):
        pass
