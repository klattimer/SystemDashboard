import json

import cherrypy
import logging

__version__ = "0.1"


class AuthenticationFailure(Exception):
    def __init__(self, message):
        super(AuthenticationFailure, self).__init__(message)

class JWTAuthTool(cherrypy.Tool):
    def __init__(self, issuer_identity, secret, auth_mech, auth_url=None, token_expires=86400, renew_window=3600):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.on_start_resource,
                               priority=20)

        self.auth_mech = auth_mech(issuer_identity, secret, token_expires, renew_window)
        self.auth_url = auth_url
        self.renew_window = renew_window

    def _setup(self):
        cherrypy.Tool._setup(self)

    def unauthorized_handler(self, status, message, traceback, version):
        if issubclass(message.__class__, dict):
            if 'redirect' in message.keys():
                # Generate redirect html
                return "<html><head><meta http-equiv=\"refresh\" content=\"10;URL='%s'\" /></head></html>" % message['redirect']
        elif self.auth_url is not None:
            return "<html><head><meta http-equiv=\"refresh\" content=\"0;URL='%s'\" /></head></html>" % self.auth_url
        raise Exception("Can't handle that")

    def on_start_resource(self, **kwargs):
        """
        Checks if the current request requires authentication
        if it requires authentication it will look for the token
        if the token doesn't exist, it will raise a redirect
        error landing on the authentication page.
        """
        args = {
            "required": False,
            "login": False
        }

        args.update(kwargs)

        if args['required'] is False:
            # Authoirzation not required to access this url
            return

        try:
            self.auth_mech.checkToken(self.auth_mech.getToken())
        except AuthenticationFailure as e:
            logging.exception("Authentication Failure")
            if cherrypy.request.headers['Accept'] != 'application/json':
                if self.auth_url is not None:
                    raise cherrypy.HTTPRedirect(self.auth_url)
                else:
                    cherrypy.response.headers['WWW-Authenticate'] = 'Basic'

            raise cherrypy.HTTPError(401, 'You are not authorized to access this resource')
