from datetime import datetime
from rotasys import db


class Staff(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    clients = db.relationship("Client", secondary="schedule")
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"Staff: {self.fullname}"


class Client(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    staff = db.relationship("Staff", secondary="schedule")
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"Client: {self.fullname}"


class Schedule(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    shift = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    staff = db.relationship(Staff, backref=db.backref("schedule", cascade="all, delete-orphan"))
    client = db.relationship(Client, backref=db.backref("schedule", cascade="all, delete-orphan"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"Schedule: {self.shift}"


class Role(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"Role: {self.title}"


class Shift(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"Role: {self.title}"







