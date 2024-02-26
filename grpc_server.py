import os
from concurrent import futures

import grpc
from sqlalchemy import create_engine

from db import Base, DatabaseSeeder
from grpc_.social_media_servicer import SocialMediaServicer
from utils import get_bool_env_variable

DB_URL = os.environ.get("DB_URL", "sqlite:///social-media.db")
USE_DB_SEED = get_bool_env_variable("USE_DB_SEED")


def run():
    engine = create_engine(DB_URL, echo=True)
    Base.metadata.create_all(engine)

    if USE_DB_SEED:
        seed = DatabaseSeeder(engine=engine)
        seed()
    engine = create_engine(DB_URL, echo=True)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=os.cpu_count()))
    servicer = SocialMediaServicer(engine=engine)
    servicer.add_to_server(server)

    port = os.environ.get("PORT", 50051)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(" ~> Server listening on port {} ...".format(port))
    server.wait_for_termination()


if __name__ == '__main__':
    run()
