# -*- coding: utf-8 -*-

__author__ = 'Karl Lattimer'
__email__ = 'karl@qdh.org.uk'
__version__ = '0.1'

from .tool import JWTAuthTool, AuthenticationFailure, RenewToken
from itsdangerous import JSONWebSignatureSerializer, BadSignature
import logging
import pam
import cherrypy
from time import time
import uuid


class BaseAuthMech:
    def __init__(self, issuer_identity, secret, expires=86400, renew_window=3600):
        self.serialiser = JSONWebSignatureSerializer(secret)
        self.expires = expires
        self.issuer_identity = issuer_identity
        self.renew_window = renew_window

    def generateToken(self, user_id):
        params = {
            'iat': int(time()),
            'iss': self.issuer_identity,
            'aud': cherrypy.request.address,
            'exp': int(time()) + self.expires,
            'sub': user_id,
            'jti': str(uuid.uuid4())
        }

        token = self.serialiser.dumps(params)
        return token

    def verifyToken(self, token):
        (scheme, token) = token.split(' ')

        def _try_decode(subject, charsets):
            for charset in charsets[:-1]:
                try:
                    return tonative(subject, charset)
                except ValueError:
                    pass
            return tonative(subject, charsets[-1])

        if scheme == "Basic":
            with cherrypy.HTTPError.handle((ValueError, binascii.Error), 400, 'Bad Request'):
                charsets = accept_charset, fallback_charset
                decoded_params = base64.b64decode(token.encode('ascii'))
                decoded_params = _try_decode(decoded_params, charsets)
                decoded_params = ntou(decoded_params)
                decoded_params = unicodedata.normalize('NFC', decoded_params)
                decoded_params = tonative(decoded_params)
                username, password = decoded_params.split(':', 1)

                if self.checkPassword(username, password):
                    token = self.generateToken(username)
                    cherrypy.request.login = username
                    cherrypy.response.headers['Authorization'] = 'Bearer ' + token.decode("utf-8")
                    cherrypy.response.cookie['Authorization'] = 'Bearer ' + token.decode("utf-8")
                    return token

            raise AuthenticationFailure("Invalid username/password in Basic token")
        elif scheme != "Bearer":
            raise AuthenticationFailure("Invalid authentication token")

        try:
            params = self.serialiser.loads(token)
        except BadSignature:
            raise AuthenticationFailure("Invalid Signature")

        if int(params['exp']) < int(time()):
            raise AuthenticationFailure("Token Expired")

        if params['aud'] != cherrypy.request.address:
            raise AuthenticationFailure("Invalid audience")

        if int(params['exp']) - self.renew_window > int(time()):
            params['exp'] = int(time()) + self.expires
            token = self.serialiser.dumps(params)
            cherrypy.response.headers['Authorization'] = 'Bearer ' + token.decode("utf-8")
            cherrypy.response.cookie['Authorization'] = 'Bearer ' + token.decode("utf-8")

        return token

    def getToken(self):
        token = None
        try:
            if 'Authorization' in cherrypy.request.cookie:
                token = cherrypy.request.cookie['Authorization']
                if 'Authorization' in cherrypy.request.headers and cherrypy.request.headers['Authorization'] != token:
                    other = cherrypy.request.headers['Authorization']
                    (scheme, data) = other.split(' ')
                    if scheme == 'Basic':
                        # We've already authenticated, the cookie will over-ride this token
                        # to avoid using the basic token again, we redirect the browser to
                        # whichever URL we tried to access and let the cookie authorize us.

                        # The request handler needs to be set in the app auth config for this
                        # to work properly.
                        raise cherrypy.HTTPError(401, {'redirect': cherrypy.url()})
            elif 'Authorization' in cherrypy.request.headers:
                token = cherrypy.request.headers['Authorization']
            elif 'Authorization' in cherrypy.request.json.keys():
                token = cherrypy.request.json['Authorization']
        except:
            logging.info("Couldn't acquire a token")
        return token

    def checkToken(self, token):
        return self.verifyToken(token)


class AuthMechInterface(BaseAuthMech):
    def checkToken(self, token):
        return super(token)

    def checkPassword(self, username, password):
        raise Exception('checkPassword required on AuthMech')


class PAMAuthMech(AuthMechInterface):

    def checkPassword(self, username, password):
        auth =  pam.pam().authenticate(username, password)
        if auth is True:
            logging.debug("Authentication Success")
        else:
            logging.debug("Authentication Failure")
        return auth
