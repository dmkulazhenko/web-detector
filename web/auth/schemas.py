from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp


class AuthSchema(Schema):
    """/auth/register [POST] & /auth/login [GET]

    Parameters:
    - Username (Str)
    - Password (Str)
    """

    username = fields.Str(
        required=True,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]"
                r"|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )
    password = fields.Str(required=True, validate=[Length(min=8, max=128)])
