from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    # Migrate debe ser inicializado después de la creación de 'app'
    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'usuarios.login'  # Set the login view

    # Import the Usuario model here to avoid circular imports
    from app.models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importa y registra Blueprints
    from app.routes.cabanas import cabanas_bp
    from app.routes.home import home_bp
    from app.routes.usuarios import usuarios_bp  # Add this line for login routes

    app.register_blueprint(cabanas_bp, url_prefix='/cabanas')
    app.register_blueprint(home_bp)
    app.register_blueprint(usuarios_bp)  # Register usuarios blueprint

    return app