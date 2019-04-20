import cherrypy
import logging

__version__ = "0.1"


class AuthenticationFailure(Exception):
    def __init__(self, message):
        super(AuthenticationFailure, self).__init__(message)


class RenewToken(Exception):
    def __init__(self, new_token):
        super(RenewToken, self).__init__()
        self.token = new_token


class JWTAuthTool(cherrypy.Tool):
    def __init__(self, secret, auth_mech, auth_url='/login', token_expires=86400, renew_window=3600):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.on_start_resource,
                               priority=20)

        self.auth_mech = auth_mech(secret, token_expires, renew_window)
        self.auth_url = auth_url
        self.renew_window = renew_window

    def _setup(self):
        cherrypy.Tool._setup(self)

    def on_start_resource(self, **kwargs):
        """
        Checks if the current request requires authentication
        if it requires authentication it will look for the token
        if the token doesn't exist, it will raise a redirect
        error landing on the authentication page.
        """
        if 'required' not in kwargs.keys() or kwargs['required'] is False:
            # Authoirzation not required to access this url
            return

        token = None
        try:
            if 'Authorization' in cherrypy.request.headers:
                token = cherrypy.request.headers['Authorization']
            if 'Authorization' in cherrypy.request.cookies:
                token = cherrypy.request.cookies['Authorization']
            if 'Authorization' in cherrypy.request.json:
                token = cherrypy.request.json['Authorization']
        except:
            logging.exception("Couldn't acquire a token")

        if token is not None:
            try:
                self.auth_mech.verifyToken(token)
            except AuthenticationFailure as e:
                raise cherrypy.HTTPRedirect(self.auth_url)
            except: RenewToken as e:
                # Set the new token on the response headers
                pass

            return

        # Get the username/password from URL
        # Get the username/password from request JSON
        # Get the username/password from
