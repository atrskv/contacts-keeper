from flask.app import Flask
from flask.cli import load_dotenv
import os
from app import routes

_ = load_dotenv()




def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')

    routes.init_app(app)

    return app
