
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user

from rotasys.auth.models import User
from rotasys import db, bcrypt

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('admin.home'))

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        if email == "" or password == "":
            flash("Email or password cannot be empty", 'info')
            return render_template("login.html", title="RotaSys | Login")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password) and user.verified:
            login_user(user, remember=True)
            next_page = request.args.get('next')
            print(next_page)
            if next_page:
                return redirect(next_page)
            return redirect(url_for('admin.home'))
        else:
            flash("Invalid Login details", "danger")
            return render_template("login.html", title="RotaSys | Login")

    return render_template("login.html", title="RotaSys | Admin Login")


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        full_name = request.form.get("fullname", "")
        if email == "" or password == "" or full_name == "":
            flash("All fields are required", 'info')
            return render_template("register.html", title="RotaSys | Login")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            user = User(fullname=full_name, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created successfully, log in!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('Email already exists.', "error")
            return redirect(url_for('auth.register'))

    return render_template("register.html", title="RotaSys | Admin Register")


@auth.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route(("/test"))
def test():

    return render_template("layout.html")

