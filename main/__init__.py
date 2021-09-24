from flask import Flask
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import secret_info
from flask_cors import CORS

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    #socket_io = SocketIO(app)
    app.config.from_object('config')
    #app.config.from_object(secret_info)
    #app.secret_key = 'sseeccrreettttttttkey'
    
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    
    CORS(app)
    from .views import index, user
    app.register_blueprint(index.bp)
    app.register_blueprint(user.bp)
    socketio.init_app(app, cors_allowed_origins="*")
    return app