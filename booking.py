from collections import namedtuple
from datetime import datetime, timezone, timedelta

Booking = namedtuple('Booking', 'datetime, main_cat, sub_cat, expense, income, description')

def datetime_str():
    now = datetime.now()
    am_pm = "上午" if now.hour < 12 else "下午"
    hour_12 = now.hour if now.hour <= 12 else now.hour - 12
    formatted_time = now.astimezone(timezone(offset=timedelta(hours=8))).strftime(f"%Y/%-m/%d {am_pm} {hour_12}:%M:%S")
    return formatted_time