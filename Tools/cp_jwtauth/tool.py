import binascii
import unicodedata
import base64
import json

import cherrypy
from cherrypy._cpcompat import ntou, tonative
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
    def __init__(self, issuer_identity, secret, auth_mech, auth_url=None, token_expires=86400, renew_window=3600):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.on_start_resource,
                               priority=20)

        self.auth_mech = auth_mech(issuer_identity, secret, token_expires, renew_window)
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
        default_args = {
            "required": False,
            "login": False
        }
        kwargs.update(default_args)

        if kwargs['required'] is False and kwargs['login'] is False:
            # Authoirzation not required to access this url
            return

        token = None
        try:
            if 'Authorization' in cherrypy.request.headers:
                token = cherrypy.request.headers['Authorization']
            elif 'Authorization' in cherrypy.request.cookie:
                token = cherrypy.request.cookie['Authorization']
        except:
            logging.exception("Couldn't acquire a token")

        if token is not None and token.startswith("Bearer"):
            logging.debug("Attempting token authorisation")
            try:
                self.auth_mech.verifyToken(token)
            except AuthenticationFailure as e:
                raise cherrypy.HTTPRedirect(self.auth_url)
            except RenewToken as e:
                # Set the new token on the response headers
                cherrypy.response.headers['Authorization'] = 'Bearer ' + e.token.decode("utf-8")
            return


        # Get the username/password from URL (authorization basic)
        accept_charset='utf-8'
        fallback_charset = 'ISO-8859-1'

        if kwargs['login'] is True and token is not None and token.startswith("Basic"):
            # split() error, base64.decodestring() error
            msg = 'Bad Request'
            with cherrypy.HTTPError.handle((ValueError, binascii.Error), 400, msg):
                scheme, params = token.split(' ', 1)
                charsets = accept_charset, fallback_charset
                decoded_params = base64.b64decode(params.encode('ascii'))
                decoded_params = _try_decode(decoded_params, charsets)
                decoded_params = ntou(decoded_params)
                decoded_params = unicodedata.normalize('NFC', decoded_params)
                decoded_params = tonative(decoded_params)
                username, password = decoded_params.split(':', 1)

                if self.auth_mech.checkpass(username, password):
                    token = self.auth_mech.generateToken(username)
                    cherrypy.request.login = username
                    cherrypy.response.headers['Authorization'] = 'Bearer ' + token.decode("utf-8")
                    return  # successful authentication


        if self.auth_url is not None:
            raise cherrypy.HTTPRedirect(self.auth_url)

        #
        # Check if the request was a JSON/API request or not
        #
        #
        if cherrypy.request.headers['Accept'] != 'application/json':
            # If we're a browser set the WWW-Authenticate header
            charset = accept_charset.upper()
            charset_declaration = (
                ('charset="%s"' % charset)
                if charset != fallback_charset
                else ''
            )
            cherrypy.response.headers['www-authenticate'] = ('Basic %s' % (charset))

        raise cherrypy.HTTPError(401, 'You are not authorized to access this resource')



def _try_decode(subject, charsets):
    for charset in charsets[:-1]:
        try:
            return tonative(subject, charset)
        except ValueError:
            pass
    return tonative(subject, charsets[-1])
