# -*- coding: utf-8 -*-

from dateutil.parser import parse as dateparse

def formatted_date(input_date):
    return '{year:04d}-{month:02d}-{day:02d}'.format(year=input_date.year, month=input_date.month, day=input_date.day)

def formatted_date_from_str(input_date_str):
    this_date = dateparse(input_date_str)
    return formatted_date(this_date)
