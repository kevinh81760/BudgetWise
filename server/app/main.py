from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes.main_routes import main
    app.register_blueprint(main)

    
