from flask import current_app
from flask_jwt_extended import create_access_token

from web import db
from web.models.user import User, UserSchema
from web.utils import err_resp, internal_err_resp, message

user_schema = UserSchema()


class AuthService:
    @staticmethod
    def login(data):
        username = data["username"]
        password = data["password"]

        try:
            if not (user := User.query.filter_by(username=username).first()):
                return err_resp(
                    "The username you have entered"
                    " does not match any account.",
                    404,
                )
            elif user and user.verify_password(password):
                user_info = user_schema.dump(user)
                access_token = create_access_token(identity=user.id)

                resp = message(True, "Successfully logged in.")
                resp["access_token"] = access_token
                resp["user"] = user_info
                return resp, 200

            return err_resp(
                "Failed to log in, password may be incorrect.", 401
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def register(data):
        username = data["username"]
        password = data["password"]

        if User.query.filter_by(username=username).first() is not None:
            return err_resp("Username is already taken.", 403)

        try:
            new_user = User(
                username=username,
                password=password,
            )
            db.session.add(new_user)
            db.session.flush()

            user_info = user_schema.dump(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.id)

            resp = message(True, "User has been registered.")
            resp["access_token"] = access_token
            resp["user"] = user_info

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
