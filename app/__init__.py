from flask import Flask
from flask_cors import CORS
import os

def create_app():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"App directory: {app_dir}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir(app_dir)}")
    
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    
    return app
