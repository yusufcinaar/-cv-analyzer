from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__,
                static_url_path='',
                static_folder='static',
                template_folder='templates')
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    
    return app
