import os
import ssl

from flask import Flask
from sqlalchemy import create_engine

from db.models import Base
from db.seed import DatabaseSeeder
from posts import posts
from users import users
from utils import get_bool_env_variable

app = Flask(__name__)

engine = create_engine(os.environ.get("DB_URL", "sqlite:///social-media.db"), echo=True)
Base.metadata.create_all(engine)

USE_DB_SEED = get_bool_env_variable("USE_DB_SEED")
if USE_DB_SEED:
    seed = DatabaseSeeder(engine=engine)
    seed()


blueprints = [users, posts]
for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    context = ssl.SSLContext()
    context.load_cert_chain('certs/cert.pem', 'certs/key.pem')
    app.run(ssl_context=context)
