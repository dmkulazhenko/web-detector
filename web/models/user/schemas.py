from web import ma

from .user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(dump_only=True)
