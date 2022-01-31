from components.utils.convert_dtypes import convert_dates_to_string, \
                                            convert_decimal_to_float
import pandas as pd
from numpy import NaN
import datetime
from random import randint, random
from decimal import Decimal

dates = [
    datetime.datetime(
        randint(2020, 2025),
        randint(1, 12),
        randint(1, 25),
        randint(0, 23),
        randint(0, 59),
        randint(0, 59)
    )
    for _ in range(50)
]

numbers = [
    Decimal(randint(0, 100) + random())
    for _ in range(50)
]

letter_choice = 'abcdefghijklmnopqrstuvwxyz'
letters = [
    letter_choice[randint(0, 25)]
    for _ in range(50)
]

df = pd.DataFrame({'a': dates, 'b': numbers, 'c': letters})


def test_can_convert_dates_to_string():
    result = convert_dates_to_string(df)
    dates = list(result['a'])
    dates = [type(date) == str for date in dates]
    assert all(dates) is True


def test_can_work_with_missing_dates():
    df.at[0, 'a'] = NaN
    result = convert_dates_to_string(df)
    dates = list(result['a'])
    dates = [type(date) == str for date in dates]
    assert all(dates) is True


def test_can_convert_decimals_to_floats():
    result = convert_decimal_to_float(df)
    floats = list(result['b'])
    floats = [type(f) == float for f in floats]
    assert all(floats) is True


def test_can_work_with_missing_decimals():
    df.at[0, 'b'] = NaN
    result = convert_decimal_to_float(df)
    floats = list(result['b'])
    floats = [type(f) == float for f in floats]
    assert all(floats) is True
