from components.utils.select_source_id import select_source_patient_id_name, \
                                              select_source_patient_id_value

import pytest


def test_can_select_source_id_name():
    result = select_source_patient_id_name('ustan')
    assert result == 'chi'


def test_can_select_source_id_value():
    result = select_source_patient_id_value('ustan', 117, 'chi')
    assert result == 1005549224


def test_can_handle_wrong_id_value():
    result = select_source_patient_id_value('ustan', 8989, 'chi')
    assert result is None
