from flask import Flask
from config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config_class)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para continuar.'

    # User loader para login_manager
    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registrar Blueprints
    from app.routes.auth_routes import bp_auth
    from app.routes.dashboard_routes import bp_dashboard
    from app.routes.citas_routes import bp_citas
    from app.routes.pacientes_routes import bp_pacientes

    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_dashboard)
    app.register_blueprint(bp_citas)
    app.register_blueprint(bp_pacientes)

    return app
