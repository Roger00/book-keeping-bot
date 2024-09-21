from collections import namedtuple
from datetime import datetime, timezone, timedelta

Booking = namedtuple('Booking', 'datetime, main_cat, sub_cat, expense, income, description, owner')

def datetime_str():
    now = datetime.now(timezone(offset=timedelta(hours=8)))
    am_pm = "上午" if now.hour < 12 else "下午"
    hour_12 = now.hour if now.hour <= 12 else now.hour - 12
    formatted_time = now.strftime(f"%Y/%-m/%d {am_pm} {hour_12}:%M:%S")
    return formatted_time