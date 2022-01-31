from components.sphr.get_source_data import tag_picker, \
                                            select_tags


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
