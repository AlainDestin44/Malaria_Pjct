from flask import Flask
from src.webapp.routes import init_routes
# from src import init_routes

def create_app():
    app = Flask(__name__)
    init_routes(app)
    return app

