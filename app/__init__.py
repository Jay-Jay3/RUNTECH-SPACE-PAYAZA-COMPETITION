import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # All The app.config[]=values

    app.config["API_TITLE"] = "My Project API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



    # Initialise database
    db.init_app(app)
    migrate.init_app(app, db)

    # importing modals
    from app import modal

    # initialise smorest api
    api = Api(app)

    # Register the routes using smorest
    # from app.routes.disputes import payaza as disputesBP
    from app.routes.escrow import payaza as escrowBP
    from app.routes.payout import payaza as payoutsBP
    from app.routes.transactions import payaza as transBP
    # from app.routes.user import payaza as userBP


    api.register_blueprint(escrowBP)
    api.register_blueprint(payoutsBP)
    api.register_blueprint(transBP)
    # api.register_blueprint(userBP)
    # api.register_blueprint(disputesBP)


    CORS(app)

    @app.route("/")
    def home():
        return "The escrow API is working"
    
    return app
    




