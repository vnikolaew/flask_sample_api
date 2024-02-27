from sqlalchemy import Engine
from sqlalchemy.orm import Session
from werkzeug.wrappers import Request, Response

from db.models import User


class AuthMiddleware(object):
    '''
    Simple WSGI middleware
    '''

    engine: Engine

    def __init__(self, app, engine):
        self.app = app
        self.engine = engine

    def __call__(self, environ, start_response):
        request = Request(environ)
        userName = request.authorization['username'] if request.authorization is not None else ''
        # password = request.authorization['password']

        with Session(self.engine) as session:
            db_user = session.query(User).where(User.username == userName).first()
            if db_user is not None:
                environ['user'] = {'name': 'Tony'}
                return self.app(environ, start_response)

            res = Response(u'Authorization failed', mimetype='text/plain', status=401)
            return res(environ, start_response)
