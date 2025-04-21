from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    # Generate a secure random key for production use
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    
    from .routes import main
    app.register_blueprint(main)
    
    return app