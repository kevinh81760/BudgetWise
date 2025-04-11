from flask import Flask
from flask_mysqldb import MySQL
from config import Config
from app.routes.main_routes import main

app = Flask(__name__) 

# Load all settings from Config class into app
app.config.from_object(Config)

# Creates a connecting handler 
mysql = MySQL(app)
# Attaches mySQL connection directly onto the Flask object 
app.mysql = mysql

app.register_blueprint(main)

if __name__ == '__main__': # Run this only if file is executed directly
    app.run(debug=True) # Start Flask in debug mode (auto-reload + error messages)

