from web import ma

from .models import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    username = ma.auto_field(dump_only=True)
