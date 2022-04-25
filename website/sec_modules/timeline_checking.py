import re

regex_date = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$'
regex_time = r'^(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)$'

def date_check(date):
    if re.fullmatch(regex_date, date):
        return True
    else:
        return False

def time_check(time):
    if re.fullmatch(regex_time, time):
        return True
    else:
        return False

