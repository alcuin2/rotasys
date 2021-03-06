from datetime import datetime
from rotasys import db


class Staff(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean(), default=False)
    address = db.Column(db.String(120), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    ni_number = db.Column(db.String(30), nullable=True)
    dbs_number = db.Column(db.String(30), nullable=True)
    clients = db.relationship("Client", secondary="schedule")
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"{self.fullname}"


class Client(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    manager = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(120), nullable=True)
    post_code = db.Column(db.String(10), nullable=True)
    active = db.Column(db.Boolean(), default=True)
    staff = db.relationship("Staff", secondary="schedule")
    date_joined = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"{self.fullname}"


class Schedule(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"))
    client_id = db.Column(db.Integer, db.ForeignKey("client.id"))
    shift = db.Column(db.String(20), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    day_number = db.Column(db.Integer)
    week_number = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime,  nullable=False)
    staff = db.relationship(Staff, backref=db.backref("schedule", cascade="all, delete-orphan"))
    client = db.relationship(Client, backref=db.backref("schedule", cascade="all, delete-orphan"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_updated = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):

        return f"{self.shift} - {self.client}"


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







