from components.data_vaults.data_vault import generate_boilerplate


def test_generate_boilerplate():
    boilerplate = generate_boilerplate()
    expected = {
        'hubs': {
            'hub_time': {'id': []},
            'hub_person': {'id': []},
            'hub_object': {'id': []},
            'hub_location': {'id': []},
            'hub_event': {'id': []}
        },
        'links': {
            'time_person_link': {
                'id': [],
                'time_id': [],
                'person_id': []
            },
            'time_object_link': {
                'id': [],
                'time_id': [],
                'object_id': []
            },
            'time_location_link': {
                'id': [],
                'time_id': [],
                'location_id': []
            },
            'time_event_link': {
                'id': [],
                'time_id': [],
                'event_id': []
            },
            'person_object_link': {
                'id': [],
                'person_id': [],
                'object_id': []
            },
            'person_location_link': {
                'id': [],
                'person_id': [],
                'location_id': []
            },
            'person_event_link': {
                'id': [],
                'person_id': [],
                'event_id': []
            },
            'object_location_link': {
                'id': [],
                'object_id': [],
                'location_id': []
            },
            'object_event_link': {
                'id': [],
                'object_id': [],
                'event_id': []
            },
            'location_event_link': {
                'id': [],
                'location_id': [],
                'event_id': []
            }
        }
    }
    assert boilerplate == expected
