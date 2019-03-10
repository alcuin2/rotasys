from datetime import datetime
from rotasys import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified = db.Column(db.Boolean(), default=False)
    password = db.Column(db.String(120), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return self.fullname
