import os
from concurrent import futures

import grpc
from sqlalchemy import create_engine

from social_media_servicer import SocialMediaServicer


def run():
    engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)
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
