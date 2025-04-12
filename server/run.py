import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from config import Config
from database import engine, Base
from models.user import User
from app.routes.auth_routes import auth

# initializes flask and loads app config
app = Flask(__name__) 
app.config.from_object(Config)

# create tables in database if they dont exist yet
Base.metadata.create_all(engine)

# register your blueprints
app.register_blueprint(auth)

if __name__ == '__main__': # Run this only if file is executed directly
    app.run(debug=True) # Start Flask in debug mode (auto-reload + error messages)

