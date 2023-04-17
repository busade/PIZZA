from flask import Flask
from .order.views import order_namespace
from .auth.views import auth_namespace
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, MethodNotAllowed


def create_app(config = config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    jwt = JWTManager(app)
    Authorizations={
        "Bearer Auth":{
                    'type':'apiKey',
                    'in':'header',
                    'name':'Authorization',
                    'description':'add a JWT with ** Bearer &lt;JWT&gt; to authorize'  
        }
    }
    api = Api(app,
            title = "Pizza Delivery API",
            description="A REST API for Pizza Delivery",
            authorizations= Authorizations,
            security= "Bearer Auth"
            )
    db.init_app(app)
    migrate = Migrate(app, db)

    api.add_namespace(order_namespace,path='/')
    api.add_namespace(auth_namespace, path='/auth')

    @api.errorhandler(NotFound)
    def Not_Found(error):
        return{"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': "Method Not Allowed"}, 405

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Order':Order
        }
    return app



