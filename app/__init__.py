from flask import Flask
from flask_cors import CORS
import os

def create_app():
    # Get the absolute path to the Flask package templates directory
    flask_dir = os.path.dirname(os.path.dirname(os.path.abspath(Flask.__file__)))
    template_dir = os.path.join(flask_dir, 'templates')
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    
    # Print debug information
    print(f"Flask package directory: {flask_dir}")
    print(f"Template directory: {template_dir}")
    print(f"Static directory: {static_dir}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Directory contents: {os.listdir()}")
    
    if os.path.exists(template_dir):
        print(f"Template directory contents: {os.listdir(template_dir)}")
    else:
        print("Template directory does not exist!")
        # Try to create and copy templates
        os.makedirs(template_dir, exist_ok=True)
        app_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        if os.path.exists(app_templates):
            import shutil
            for item in os.listdir(app_templates):
                src = os.path.join(app_templates, item)
                dst = os.path.join(template_dir, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"Copied {item} to {template_dir}")
    
    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)
    CORS(app)
    
    from .routes import main
    app.register_blueprint(main, url_prefix='/')
    
    return app
