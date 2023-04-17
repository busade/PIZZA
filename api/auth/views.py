from flask_restx import Namespace, Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import check_password_hash, generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import jwt_required,create_access_token, create_refresh_token, get_jwt_identity
from werkzeug.exceptions import Conflict, BadRequest
auth_namespace= Namespace('auth', description="Namespace for authentication")


auth_model =auth_namespace.model(
            "User", {
                'id': fields.Integer(),
                "username":fields.String(required=True, description= "A username"),
                "email":fields.String(required=True,description="User's email"),
                "password_hash":fields.String(required=True, description="User's password")
            }
)

login_model = auth_namespace.model(
                'Login',{
                    'email': fields.String(required = True, Description = "User's email"),
                    'password_hash':fields.String(required= True, Description=' A password')

                }
)


@auth_namespace.route('/signup')
class SignUp(Resource):

    @auth_namespace.expect(auth_model)
    @auth_namespace.marshal_with(auth_model)
    def post (self):
        """Create a new User"""
        data = request.get_json()
        try:
            new_user= User(
            email=data.get('email'),
            username= data.get('username'),
            password_hash=generate_password_hash(data.get('password_hash'))
        )
            new_user.save()
            return new_user, HTTPStatus.CREATED
        except Exception as e:
            raise Conflict (f"User with {data.get('email')} exists")

@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    def post(self):
        """Generate JWT"""
        data = request.get_json()
        email = data.get('email')
        password_hash= data.get('password_hash')
        user = User.query.filter_by(email=email).first()
        
        if (user is not None )and check_password_hash(pwhash=user.password_hash,password=password_hash):
            access_token = create_access_token(identity = user.username)
            refresh_token = create_refresh_token(identity = user.username)

            response={
                    "access_token":access_token,
                    "refresh_token":refresh_token
            }
            return response, HTTPStatus.OK
        else:
            return {'message': "email or password is invalid "},HTTPStatus.BAD_REQUEST

@auth_namespace.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def refresh(self):
        username = get_jwt_identity()

        access_token = create_access_token(identity = username)
        return access_token,HTTPStatus.ok
