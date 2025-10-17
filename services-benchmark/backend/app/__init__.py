from flask import Flask
from .extensions import mongo
from .routes.submissions_routes import submissions_bp
from .routes.assignments_routes import assignments_bp
from .routes.monitoring_routes import monitoring_bp
from .error_handlers import register_error_handlers
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #start mongo
    mongo.init_app(app)

    #Create upload directory
    Config.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    #Create blueprints
    app.register_blueprint(submissions_bp, url_prefix='/api')
    app.register_blueprint(assignments_bp, url_prefix='/api')
    app.register_blueprint(monitoring_bp, url_prefix='/api')

    #start handler of error
    register_error_handlers(app)

    @app.route('/')
    def index():
        return{
            "service": "Assignment Submission Service",
            "version": "1.0.0"
        }
    return app
