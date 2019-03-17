import datetime
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, logout_user, current_user, login_required

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


@auth.route("/user/create", methods=['GET', 'POST'])
#@login_required
def create_user():
    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        full_name = request.form.get("fullname", "")
        if email == "" or password == "" or full_name == "":
            flash("All fields are required", 'info')
            return render_template("register.html", title="RotaSys | Login")
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        try:
            user = User(fullname=full_name, email=email, password=hashed_password, verified=True)
            db.session.add(user)
            db.session.commit()
            flash('User has been created successfully!', 'success')
            return redirect(url_for('auth.all_users'))
        except:
            flash('Email already exists.', "error")
            return redirect(url_for('auth.create_user'))

    return render_template("create_user.html", title="RotaSys | Admin Register")


@auth.route("/users/all")
@login_required
def all_users():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.date_joined.desc()).paginate(page=page, per_page=20)
    return render_template("all_users.html", users=users)


@auth.route("/user/edit/<int:user_id>", methods=["POST", "GET"])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return render_template("404.html", title="RotaSys | Not Found")
    if request.method == "POST":
        form_dict = request.form.to_dict()
        user.fullname = form_dict["fullname"]
        user.email = form_dict["email"]
        if request.form.get("active", "") == "1":
            user.verified = True
        else:
            user.verified = False
        user.date_updated = datetime.datetime.utcnow()
        db.session.commit()
        flash("Staff edited", "success")
        return redirect(url_for("auth.all_users"))

    return render_template("edit_user.html", user=user)


@auth.route("/user/delete/<int:user_id>")
@login_required
def delete_user(user_id):

    user = User.query.get(user_id)
    if user is None:
        return render_template("404.html", title="RotaSys | Not Found")
    db.session.delete(user)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("auth.all_users"))


@auth.route("/logout")
def logout():

    logout_user()
    return redirect(url_for('auth.login'))


'''
@auth.route("/test")
def test():

    return render_template("layout.html")
'''

