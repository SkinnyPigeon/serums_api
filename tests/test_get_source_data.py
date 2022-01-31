from components.sphr.get_source_data import tag_picker, \
                                            select_tags, \
                                            select_tabular_patient_data, \
                                            parse_sphr, \
                                            setup_for_query
from tests.test_jwt_validation import JWT
from tests.test_valid_staff_jwt import right_jwt as staff_jwt
import json


def test_tag_picker():
    tags = tag_picker('ustan')
    assert type(tags) == list
    assert len(tags) > 0
    assert type(tags[0]) == dict


def test_select_tags():
    tags = tag_picker('ustan')
    single_table_request_tags = [
        'patient_details',
        'chemotherapy'
    ]
    results = select_tags(tags, single_table_request_tags)
    assert len(results) == 2
    assert type(results[0]) == dict
    multi_table_request_tags = {
        'medication'
    }
    results = select_tags(tags, multi_table_request_tags)
    assert len(results) == 3
    assert type(results[0]) == dict


def test_tag_selection_can_handle_wrong_tags():
    tags = tag_picker('ustan')
    wrong_tags = [
        'this',
        'is',
        'wrong'
    ]
    results = select_tags(tags, wrong_tags)
    assert len(results) == 0
    wrong_tags.append('patient_details')
    results = select_tags(tags, wrong_tags)
    assert len(results) == 1
    assert type(results[0]) == dict


def test_can_select_tabular_data():
    tags = tag_picker('ustan')
    request_tags = ['patient_details']
    tag_definitions = select_tags(tags, request_tags)
    result = select_tabular_patient_data(
        tag_definitions[0],
        1005549224,
        'chi'
    )
    assert len(result) > 0
    assert 'chi' in result[0].keys()
    assert 'name' in result[0].keys()


def test_can_parse_data():
    tags = tag_picker('ustan')
    request_tags = ['patient_details']
    tag_definitions = select_tags(tags, request_tags)
    result = select_tabular_patient_data(
        tag_definitions[0],
        1005549224,
        'chi'
    )
    example = {}
    example['ustan'] = {}
    example['ustan']['data'] = {}
    example['ustan']['data'][tag_definitions[0]['source']] = result
    parsed_data = parse_sphr(example)
    dob = parsed_data['ustan'][tag_definitions[0]['source']][0]['dob']
    assert dob == '1954-05-10'
    json_data = json.dumps(parsed_data)
    assert type(json_data) == str


def test_setup_for_query():
    tags = ['patient_details', 'medication']
    hospital_ids = ['ustan']
    proof_id, valid_tags, rule_ids = setup_for_query(
        JWT,
        tags,
        117,
        hospital_ids
    )
    assert proof_id[:6] == 'PROOF_'
    assert valid_tags == tags
    assert rule_ids == 'PATIENT-ACCESSING-OWN-RECORD'
    tags.append('secret_data')
    proof_id, valid_tags, rule_ids = setup_for_query(
        staff_jwt,
        tags,
        117,
        hospital_ids
    )
    assert proof_id[:6] == 'PROOF_'
    assert valid_tags == ['patient_details']
