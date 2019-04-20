# -*- coding: utf-8 -*-

__author__ = 'Karl Lattimer'
__email__ = 'karl@qdh.org.uk'
__version__ = '0.1'

from .tool import JWTAuthTool, AuthenticationFailure
from itsdangerous import JSONWebSignatureSerializer, BadSignature
import logging
import pam
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
            'exp': int(time()) + self.expires,
            'sub': user_id,
            'jti': str(uuid.uuid4()),
            'https://': True,
        }

        token = self.serialiser.dumps(params)
        return token

    def verifyToken(self, token):
        try:
            params = self.serialiser.loads(token)
        except BadSignature:
            raise AuthenticationFailure("Invalid Signature")

        if int(params['exp']) > int(time()) - self.renew_window:
            raise RenewToken(self.renewToken(params))

        if int(params['exp']) < int(time()):
            raise AuthenticationFailure("Token Expired")

        return token

    def renewToken(self, params):
        params['exp'] = int(time()) + expires
        token = self.serialiser.dumps(params)
        return token

class AuthMechInterface(BaseAuthMech):

    def checkpass(self, username, password):
        raise Exception('checkpass required on AuthMech')


class PAMAuthMech(AuthMechInterface):

    def checkpass(self, username, password):
        auth =  pam.pam().authenticate(username, password)
        if auth is True:
            logging.debug("Authentication Success")
        else:
            logging.debug("Authentication Failure")
        return auth
