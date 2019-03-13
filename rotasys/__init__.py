from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from rotasys.middleware import ReverseProxied

csrf = CsrfProtect()

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

app.config["SECRET_KEY"] = "63dc08a349bdb03a2ejcgvdudvdjvyfvdjcjdbdgccldbdkghd"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = "info"
login_manager.login_message = "Please log in to access this page"


csrf.init_app(app)

from rotasys.auth.routes import auth
from rotasys.admin.routes import admin
from rotasys.admin import filters

app.register_blueprint(auth)
app.register_blueprint(admin)

