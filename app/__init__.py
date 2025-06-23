from flask import Flask
from flask_cors import CORS
import os

def create_app():
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))
    
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    
    return app
