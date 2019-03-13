from rotasys import app
from rotasys.admin.models import Client, Schedule, Staff


@app.template_filter()
def get_client_from_schedule(schedule_id):
    schedule = Schedule.query.get(schedule_id)
    client = Client.query.get(schedule.client_id)
    return client.fullname


@app.template_filter()
def get_staff_from_schedule(staff_id):
    staff = Staff.query.get(staff_id)
    return staff.fullname


@app.template_filter()
def get_staff_role(staff_id):
    staff = Staff.query.get(staff_id)
    return staff.role


@app.template_filter()
def format_schedules(schedule_list):
    if len(schedule_list) == 1:
        return schedule_list[0]
    elif len(schedule_list) == 0:
        return None
    else:
        start_str = ""
        for item in schedule_list:
            start_str = start_str + str(item) + "<br />"
        return start_str





