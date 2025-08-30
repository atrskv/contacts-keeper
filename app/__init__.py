import os
from app.data import generate_initial_data
from app.routes.api import init_api
from app.routes.ui import init_ui
from flask import Flask
from flask.json.provider import DefaultJSONProvider
from dotenv import load_dotenv

class JSONProvider(DefaultJSONProvider):
    def dumps(self, obj, **kwargs):
        kwargs.setdefault('ensure_ascii', False)
        return super().dumps(obj, **kwargs)

    def loads(self, s, **kwargs):
        return super().loads(s, **kwargs)


_ = load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    
    app.json_provider_class = JSONProvider
    app.json = app.json_provider_class(app)
    
 
    init_ui(app)
    init_api(app)
    
    generate_initial_data() 

    return app
