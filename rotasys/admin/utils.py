from dateutil import relativedelta

days = {
    1: "MONDAY",
    2: "TUESDAY",
    3: "WEDNESDAY",
    4: "THURSDAY",
    5: "FRIDAY",
    6: "SATURDAY",
    7: "SUNDAY"
}

months = {
    1: "JANUARY",
    2: "FEBRUARY",
    3: "MARCH",
    4: "APRIL",
    5: "MAY",
    6: "JUNE",
    7: "JULY",
    8: "AUGUST",
    9: "SEPTEMBER",
    10: "OCTOBER",
    11: "NOVEMBER",
    12: "DECEMBER"
}


def get_week_number(date):

    return date.isocalendar()[1]


def get_week_day(date):

    number = date.isocalendar()[2]
    return days[number]


def get_month(date):

    number = date.month
    return months[number]


def get_year(date):

    return date.isocalendar()[0]


def get_start_date(week_number):
    pass


def get_end_date(week_number):
    pass


