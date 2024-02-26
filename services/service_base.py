from sqlalchemy import Engine
from sqlalchemy.orm import Session


class ServiceBase(object):
    engine: Engine
    session: Session

    def __init__(self, engine: Engine):
        self.engine = engine

    def __enter__(self):
        self.session = Session(self.engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
