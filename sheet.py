import gspread
from collections import namedtuple
from typing import NamedTuple

Booking = namedtuple('Booking', 'datetime, main_cat, sub_cat, expense, income, description')

SPREADSHEET_ID = '1xBp1arSbr-qX4t0tQirVtvjdMgR5_R4-WoIezaoquyM'

def append_booking(b: NamedTuple):
    gc = gspread.service_account()
    wks = gc.open_by_key(SPREADSHEET_ID).sheet1
    wks.append_row([b.datetime, '', b.main_cat, b.sub_cat, b.expense, b.income, b.description], table_range="A1:G1")


def main():
    b = Booking(datetime=1726899449, main_cat='食品酒水', sub_cat='午餐', expense=7, income=0, description='鐵男家')
    append_booking(b)

if __name__ == '__main__':
    main()