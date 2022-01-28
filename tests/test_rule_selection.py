from components.blockchain.rules import get_rules, \
                                        validate_doctor, \
                                        sum_up_rules, \
                                        get_valid_tags
from tests.test_valid_staff_jwt import right_jwt


def test_can_get_rules():
    rules = get_rules(right_jwt, 117, 120)
    assert len(rules) > 0
    assert type(rules[0]) == dict
    assert rules[0]['action'] in ['ALLOW', 'DENY']


def test_can_validate_doctor():
    assert validate_doctor(['MEDICAL_STAFF']) is True
    assert validate_doctor(['PATIENT']) is False


def test_can_sum_up_rules():
    rules = get_rules(right_jwt, 117, 120)
    tags = sum_up_rules(rules)
    assert len(tags) > 0
    assert len(tags) < len(rules)
    assert 'patient_details' in tags
    assert 'medication' not in tags


def test_can_get_valid_tags():
    tags, rule_ids = get_valid_tags(right_jwt, 117)
    assert len(tags) > 0
    assert 'patient_details' in tags
    assert 'medication' not in tags
