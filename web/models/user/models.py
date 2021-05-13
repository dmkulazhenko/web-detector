from web import bcrypt, db

Column = db.Column
Model = db.Model


class User(Model):
    id = Column(db.Integer, primary_key=True)
    username = Column(db.String(15), unique=True, index=True)
    password_hash = Column(db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
