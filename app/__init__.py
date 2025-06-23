from flask import Flask
from flask_cors import CORS
import os

def create_app():
    # Get the absolute path to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define template and static folder paths relative to app directory
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    # Print debug information
    print(f"App directory: {app_dir}")
    print(f"Template directory: {template_dir}")
    print(f"Static directory: {static_dir}")
    
    if os.path.exists(template_dir):
        print(f"Template directory contents: {os.listdir(template_dir)}")
    else:
        print("Template directory does not exist!")
    
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    
    return app
