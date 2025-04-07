from flask import Flask
from app.routes.main_routes import main

app = Flask(__name__) 

app.register_blueprint(main)

if __name__ == '__main__': # Run this only if file is executed directly
    app.run(debug=True) # Start Flask in debug mode (auto-reload + error messages)

