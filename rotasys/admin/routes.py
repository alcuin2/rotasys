import datetime
from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user

from rotasys import db
from rotasys.admin.models import Staff, Client, Schedule, Role, Shift
from rotasys.auth.models import User

from rotasys.admin.utils import get_week_day, get_week_number, get_month, get_year

admin = Blueprint("admin", __name__)


@admin.route("/")
@login_required
def home():

    staff = Staff.query.all()
    clients = Client.query.all()
    schedules = Schedule.query.all()
    roles = Role.query.all()
    users = User.query.all()
    shifts = Shift.query.all()

    return render_template("home.html", title="RotaSys | Dashboard",
                           staff=staff, clients=clients, schedules=schedules,
                           roles=roles, users=users, shifts=shifts)


@admin.route("/staff/create", methods=["POST", "GET"])
@login_required
def create_staff():

    roles = Role.query.all()
    if request.method == "POST":
        form_dict = request.form.to_dict()
        new_staff = Staff(fullname=form_dict["fullname"], email=form_dict["email"], active=True, role=form_dict["role"])
        db.session.add(new_staff)
        db.session.commit()
        flash("New staff added successfully", "success")
        return redirect(url_for("admin.create_staff"))

    return render_template("create_staff.html", title="RotaSys | Create New Staff", roles=roles)


@admin.route("/staff/<int:staff_id>")
@login_required
def read_staff(staff_id):

    staff = Staff.query.get(staff_id)
    if staff is None:
        return render_template("404.html", title="RotaSys | Not Found")
    return render_template("staff_details.html", title="RotaSys | Staff Details", staff=staff)


@admin.route("/staff/all")
@login_required
def all_staff():

    page = request.args.get('page', 1, type=int)
    staff = Staff.query.order_by(Staff.date_updated.desc()).paginate(page=page, per_page=20)
    return render_template("all_staff.html", staff=staff)


@admin.route("/staff/delete/<int:staff_id>")
@login_required
def delete_staff(staff_id):

    staff = Staff.query.get(staff_id)
    if staff is None:
        return render_template("404.html", title="RotaSys | Not Found")
    db.session.delete(staff)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.all_staff"))


@admin.route("/client/create", methods=["POST", "GET"])
@login_required
def create_client():

    if request.method == "POST":
        form_dict = request.form.to_dict()
        new_client = Client(fullname=form_dict["fullname"], email=form_dict["email"], active=True)
        db.session.add(new_client)
        db.session.commit()
        flash("New client added successfully", "success")
        return redirect(url_for("admin.create_client"))

    return render_template("create_client.html", title="RotaSys | Create New Client")


@admin.route("/client/<int:client_id>")
@login_required
def read_client(client_id):

    client = Client.query.get(client_id)
    if client is None:
        return render_template("404.html", title="RotaSys | Not Found")
    return render_template("client_details.html", title="RotaSys | Client Details", client=client)


@admin.route("/client/all")
@login_required
def all_clients():

    page = request.args.get('page', 1, type=int)
    clients = Client.query.order_by(Client.date_updated.desc()).paginate(page=page, per_page=20)
    return render_template("all_clients.html", clients=clients)


@admin.route("/client/delete/<int:client_id>")
@login_required
def delete_client(client_id):

    client = Staff.query.get(client_id)
    if client is None:
        return render_template("404.html", title="RotaSys | Not Found")
    db.session.delete(client)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.all_clients"))


@admin.route("/role/create", methods=["POST", "GET"])
@login_required
def create_role():

    if request.method == "POST":
        form_dict = request.form.to_dict()
        new_role = Role(title=form_dict["title"])
        db.session.add(new_role)
        db.session.commit()
        flash("New role added successfully", "success")
        return redirect(url_for("admin.create_role"))

    return render_template("create_role.html", title="RotaSys | Create New Role")


@admin.route("/role/<int:role_id>")
@login_required
def read_role(role_id):

    role = Role.query.get(role_id)
    if role is None:
        return render_template("404.html", title="RotaSys | Not Found")
    return render_template("role_details.html", title="RotaSys | Client Details", role=role)


@admin.route("/role/all")
@login_required
def all_roles():

    page = request.args.get('page', 1, type=int)
    roles = Role.query.order_by(Role.date_updated.desc()).paginate(page=page, per_page=20)
    return render_template("all_roles.html", roles=roles)


@admin.route("/role/delete/<int:role_id>")
@login_required
def delete_role(role_id):

    role = Role.query.get(role_id)
    if role is None:
        return render_template("404.html", title="RotaSys | Not Found")
    db.session.delete(role)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.all_roles"))


@admin.route("/shift/create", methods=["POST", "GET"])
@login_required
def create_shift():

    if request.method == "POST":
        form_dict = request.form.to_dict()
        new_shift = Shift(title=form_dict["title"])
        db.session.add(new_shift)
        db.session.commit()
        flash("New shift added successfully", "success")
        return redirect(url_for("admin.create_shift"))

    return render_template("create_shift.html", title="RotaSys | Create New Shift")


@admin.route("/shifts/all")
@login_required
def all_shifts():

    page = request.args.get('page', 1, type=int)
    shifts = Shift.query.order_by(Shift.date_updated.desc()).paginate(page=page, per_page=20)
    return render_template("all_shifts.html", shifts=shifts)


@admin.route("/shift/delete/<int:shift_id>")
@login_required
def delete_shift(shift_id):

    shift = Shift.query.get(shift_id)
    if shift is None:
        return render_template("404.html", title="RotaSys | Not Found")
    db.session.delete(shift)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.all_shifts"))


@admin.route("/schedule/create", methods=["POST", "GET"])
@login_required
def create_schedule():

    if request.method == "POST":
        form_dict = request.form.to_dict()
        shift = form_dict["shift"]
        date_string = form_dict["date"]
        date = datetime.strptime(date_string, "%d/%m/%Y").date()
        week_number = get_week_number(date)
        day = get_week_day(date)
        month = get_month(date)
        year = get_year(date)
        new_schedule = Schedule(staff_id=form_dict["staff_id"],
                                client_id=form_dict["client_id"],
                                shift=shift,
                                week_number=week_number,
                                day=day,
                                month=month,
                                year=year)
        db.session.add(new_schedule)
        db.session.commit()
        flash("New schedule added successfully", "success")
        return redirect(url_for("admin.create_schedule"))

    return render_template("create_role.html", title="RotaSys | Create Schedule")













