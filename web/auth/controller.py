from flask import request
from flask_restx import Resource

from web.utils import validation_error

from .dto import AuthDto
from .schemas import AuthSchema
from .service import AuthService

api = AuthDto.api

auth_schema = AuthSchema()


@api.route("/login")
class AuthLogin(Resource):
    """User login endpoint."""

    @api.doc(
        "Auth login",
        responses={
            200: ("Logged in.", AuthDto.auth_success),
            400: "Validations failed.",
            403: "Incorrect password or incomplete credentials.",
            404: "Username does not match any account.",
        },
    )
    @api.expect(AuthDto.auth_login, validate=True)
    def post(self):
        """Login using username and password."""
        login_data = request.get_json()

        if errors := auth_schema.validate(login_data):
            return validation_error(False, errors), 400

        return AuthService.login(login_data)


@api.route("/register")
class AuthRegister(Resource):
    """User register endpoint."""

    @api.doc(
        "Auth registration",
        responses={
            201: ("Successfully registered user.", AuthDto.auth_success),
            400: "Malformed data or validations failed.",
        },
    )
    @api.expect(AuthDto.auth_register, validate=True)
    def post(self):
        """User registration."""
        register_data = request.get_json()

        if errors := auth_schema.validate(register_data):
            return validation_error(False, errors), 400

        return AuthService.register(register_data)
