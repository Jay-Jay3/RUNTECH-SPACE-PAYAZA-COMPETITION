import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # All The app.config[]=values



    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


    database_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)



    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)








    app.config["API_TITLE"] = "My Project API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    # app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    # Initialise database
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # importing modals
    from app import modal

    #configuring smorest(SWAGGER_UI)
    app.config["OPENAPI_URL_PREFIX"]= "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"]= "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"]= "https://unpkg.com/swagger-ui-dist@3.25.0/"

    # initialise smorest api
    api = Api(app)

    # Register the routes using smorest
    # from app.routes.disputes import payaza as disputesBP
    from app.routes.escrow import payaza as escrowBP
    from app.routes.payout import payaza as payoutsBP
    from app.routes.transactions import payaza as transBP
    from app.routes.user import payaza as userBP


    api.register_blueprint(escrowBP)
    api.register_blueprint(payoutsBP)
    api.register_blueprint(transBP)
    api.register_blueprint(userBP)
    # api.register_blueprint(disputesBP)


    CORS(app)


    @login_manager.user_loader
    def load_user(user_id):
        from app.modal import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to JSON 401 instead of login page."""
        return jsonify({"error": "Unauthorized", "message": "Please log in to access this resource"}), 401

    @app.route("/")
    def home():
        return "The escrow API is working"
    
    return app
    




