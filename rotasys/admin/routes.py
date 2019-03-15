import datetime
import os
from flask import Blueprint, render_template, url_for, request, flash, redirect, send_file
from flask_login import login_required, current_user

from rotasys import db
from rotasys.admin.models import Staff, Client, Schedule, Role, Shift
from rotasys.auth.models import User

from rotasys.admin.utils import (get_week_day, get_week_number, get_month, get_year,
                                 get_start_date, get_end_date)

from rotasys.admin.utils import days

admin = Blueprint("admin", __name__)


@admin.route("/")
@admin.route("/<int:week_number>")
@login_required
def home(week_number=None):

    staff = Staff.query.all()
    clients = Client.query.all()
    schedules = Schedule.query.all()
    roles = Role.query.all()
    users = User.query.all()
    shifts = Shift.query.all()

    if week_number is None:
        date = datetime.datetime.utcnow()
        week_number = date.isocalendar()[1]
        year = date.isocalendar()[0]
    query = db.session.query(Schedule.staff_id.distinct().label("staff_id"))
    staff_ids = [row.staff_id for row in query.all()]
    schedules_ = []
    for staff_id in staff_ids:
        weekdays = []
        for day in days.values():
            staff_schedules_ = Schedule.query.filter_by(staff_id=staff_id).filter_by(week_number=week_number).\
                filter_by(year=year).filter_by(day=day).order_by(Schedule.day_number.asc()).all()
            weekdays.append(staff_schedules_)

        schedules_.append({"staff_id": staff_id, "days": weekdays})

    start_date = get_start_date(week_number)
    end_date = get_end_date(week_number)

    return render_template("home.html", title="RotaSys | Dashboard",
                           staff=staff, clients=clients, schedules=schedules,
                           schedules_=schedules_, week_number=week_number,
                           roles=roles, users=users, shifts=shifts, year=year)


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


@admin.route("/staff/edit/<int:staff_id>", methods=["POST", "GET"])
def edit_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if staff is None:
        return render_template("404.html", title="RotaSys | Not Found")
    roles = Role.query.all()
    if request.method == "POST":
        form_dict = request.form.to_dict()
        print(form_dict)
        staff.fullname = form_dict["fullname"]
        staff.email = form_dict["email"]
        staff.role = form_dict["role"]
        if request.form.get("active", "") == "1":
            staff.active = True
        else:
            staff.active = False
        staff.date_updated = datetime.datetime.utcnow()
        db.session.commit()
        flash("Staff edited", "success")
        return redirect(url_for("admin.all_staff"))

    return render_template("edit_staff.html", staff=staff, roles=roles)


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


@admin.route("/schedule/staff/<int:staff_id>", methods=["POST", "GET"])
@login_required
def add_staff_schedule(staff_id):

    staff = Staff.query.get(staff_id)
    if staff is None:
        return render_template("404.html", title="RotaSys | Not Found")
    clients = Client.query.all()
    shifts = Shift.query.all()
    if request.method == "POST":
        form_dict = request.form.to_dict()
        print(form_dict)
        date_string = form_dict["date"]
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        week_number = get_week_number(date)
        day = get_week_day(date)
        month = get_month(date)
        year = get_year(date)
        new_schedule = Schedule(staff_id=staff.id,
                                client_id=form_dict["client"],
                                shift=form_dict["shift"],
                                day_number=date.isocalendar()[2],
                                date=date,
                                week_number=week_number,
                                day=day,
                                month=month,
                                year=year)
        db.session.add(new_schedule)
        db.session.commit()
        flash("New schedule added successfully", "success")
        return redirect(url_for("admin.add_staff_schedule", staff_id=staff.id))

    return render_template("staff_add_schedule.html", title="RotaSys | Create Schedule", staff=staff,
                           clients=clients, shifts=shifts)


@admin.route("/schedule/staff/all/<int:staff_id>")
def staff_schedules(staff_id):

    staff = Staff.query.get(staff_id)
    if staff is None:
        return render_template("404.html", title="RotaSys | Not Found")
    page = request.args.get('page', 1, type=int)

    schedules = Schedule.query.filter_by(staff_id=staff.id).order_by(Schedule.date_updated.desc())\
        .paginate(page=page, per_page=20)
    return render_template("all_schedules.html", staff=staff, schedules=schedules)


@admin.route("/schedule/delete/<int:schedule_id>")
def delete_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if schedule is None:
        return render_template("404.html", title="RotaSys | Not Found")

    db.session.delete(schedule)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.staff_schedules", staff_id=schedule.staff_id))


@admin.route("/schedule/edit/<int:schedule_id>")
def edit_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    if schedule is None:
        return render_template("404.html", title="RotaSys | Not Found")

    db.session.delete(schedule)
    db.session.commit()
    flash("Delete successful", "info")
    return redirect(url_for("admin.staff_schedules", staff_id=schedule.staff_id))



'''
@admin.route("/rota/generate/<int:week_number>")
@admin.route("/rota/generate")
def generate_rota(week_number=None):

    if week_number is None:
        date = datetime.datetime.utcnow()
        week_number = date.isocalendar()[1]
    query = db.session.query(Schedule.staff_id.distinct().label("staff_id"))
    staff_ids = [row.staff_id for row in query.all()]
    schedules = []
    for staff in staff_ids:
        weekdays = []
        for day in days.values():
            staff_schedules_ = Schedule.query.filter_by(staff_id=staff).filter_by(week_number=week_number)\
                .filter_by(day=day).order_by(Schedule.day_number.asc()).all()
            weekdays.append(staff_schedules_)

        schedules.append({"staff_id": staff, "days": weekdays})

    start_date = get_start_date(week_number)
    end_date = get_end_date(week_number)
    return render_template("rota.html", schedules=schedules, week_number=week_number)
'''


@admin.route("/download/timesheet")
def download_timesheet():

    return redirect("rota/static/assets/files/timesheet.pdf")


@admin.route("/download/report/<int:week_number>/<int:year>")
def download_report(week_number, year):
    pass





