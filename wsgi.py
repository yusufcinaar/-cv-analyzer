import os
from app import create_app

# Projenin kök dizinine geç
os.chdir(os.path.dirname(os.path.abspath(__file__)))

app = create_app()

if __name__ == '__main__':
    app.run()
