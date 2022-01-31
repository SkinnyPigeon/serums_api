from py import process
from components.data_vaults.data_vault import generate_boilerplate, \
                                              get_id_columns, \
                                              create_data_vault
from components.data_vaults.satellites import process_value, \
                                              process_satellites
from components.data_vaults.hub_post_processing import hub_equalizer
from components.data_vaults.link_post_processing import add_id_values
from components.sphr.get_source_data import get_patient_data
from tests.test_valid_staff_jwt import right_jwt as staff_jwt
from tests.test_jwt_validation import JWT as patient_jwt
import datetime
import decimal


def test_get_id_columns():
    result_one = get_id_columns('time_person_link')
    result_two = get_id_columns('person_object_link')
    assert result_one == {'id': [], 'time_id': [], 'person_id': []}
    assert result_two == {'id': [], 'person_id': [], 'object_id': []}


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


def test_process_value():
    val_one = process_value(datetime.datetime(1984, 8, 7))
    val_two = process_value("Hello     ")
    val_three = process_value(datetime.time(11, 38, 48))
    val_four = process_value(decimal.Decimal(12378.12237823727319))
    assert val_one == '07/08/1984 00:00:00'
    assert val_two == "Hello"
    assert val_three == '11:38:48'
    assert val_four == 12378.122378237273


def test_process_satellites():
    data, _ = get_patient_data(
        117,
        ['ustan'],
        ['patient_details', 'medication', 'wearable'],
        staff_jwt
    )
    result = process_satellites(data)
    expected = {
        'USTAN': {
            'ustan.general': {
                'links': [
                    'time_person_link',
                    'time_location_link',
                    'time_event_link',
                    'person_location_link',
                    'person_event_link',
                    'location_event_link'
                ],
                'sat_time_general_details': {
                    'hub': 'hub_time',
                    'data': [
                        {
                            'first_seen_date': '18/04/2017 00:00:00',
                            'dat_death': None
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_person_general_patient': {
                    'hub': 'hub_person',
                    'data': [
                        {
                            'name': 'HERMIONE KOCZUR',
                            'date_of_birth': '10/05/1954 00:00:00',
                            'dob': '10/05/1954 00:00:00',
                            'gender': 2,
                            'religion': 0,
                            'civil_st': 9,
                            'postcode': 'KY953HY'
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_person_general_gp': {
                    'hub': 'hub_person',
                    'data': [{}],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_location_general_details': {
                    'hub': 'hub_location',
                    'data': [
                        {
                            'ref_hospital': 617
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                },
                'sat_event_general_details': {
                    'hub': 'hub_event',
                    'data': [
                        {
                            'smid': None,
                            'smid1': None,
                            'death_flag': 0
                        }
                    ],
                    'keys': [
                        {
                            'chi': 1005549224
                        }
                    ]
                }
            }
        }
    }
    assert type(result) == dict
    assert result == expected


def test_can_create_data_vault():
    data, _ = get_patient_data(
        117,
        ['ustan'],
        ['patient_details', 'medication', 'wearable'],
        staff_jwt
    )
    sats = process_satellites(data)
    result = create_data_vault(sats)
    expected = {
        'satellites': {
            'ustan_sat_time_general_details': [
                {
                    'first_seen_date': '18/04/2017 00:00:00',
                    'dat_death': None,
                    'hub_time_id': 1
                }
            ],
            'ustan_sat_person_general_patient': [
                {
                    'name': 'HERMIONE KOCZUR',
                    'date_of_birth':
                    '10/05/1954 00:00:00',
                    'dob': '10/05/1954 00:00:00',
                    'gender': 2,
                    'religion': 0,
                    'civil_st': 9,
                    'postcode': 'KY953HY',
                    'hub_person_id': 1
                }
            ],
            'ustan_sat_person_general_gp': [
                {
                    'hub_person_id': 1
                }
            ],
            'ustan_sat_location_general_details': [
                {
                    'ref_hospital': 617,
                    'hub_location_id': 1
                }
            ],
            'ustan_sat_event_general_details': [
                {
                    'smid': None,
                    'smid1': None,
                    'death_flag': 0,
                    'hub_event_id': 1
                }
            ]
        },
        'hubs': {
            'hub_time': {
                'id': [1],
                'chi': [1005549224]
            },
            'hub_person': {
                'id': [1, 1],
                'chi': [1005549224, 1005549224]
            },
            'hub_object': {
                'id': []
            },
            'hub_location': {
                'id': [1],
                'chi': [1005549224]
            },
            'hub_event': {
                'id': [1],
                'chi': [1005549224]
            }
        },
        'links': {
            'time_person_link': {
                'id': [],
                'time_id': [1],
                'person_id': [1]
            },
            'time_object_link': {
                'id': [],
                'time_id': [],
                'object_id': []
            },
            'time_location_link': {
                'id': [],
                'time_id': [1],
                'location_id': [1]
            },
            'time_event_link': {
                'id': [],
                'time_id': [1],
                'event_id': [1]
            },
            'person_object_link': {
                'id': [],
                'person_id': [],
                'object_id': []
            },
            'person_location_link': {
                'id': [],
                'person_id': [1],
                'location_id': [1]
            },
            'person_event_link': {
                'id': [],
                'person_id': [1],
                'event_id': [1]
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
                'location_id': [1],
                'event_id': [1]
            }
        }
    }
    assert result == expected


def test_can_equalize_data_vault():
    data, _ = get_patient_data(
        117,
        ['ustan'],
        ['patient_details', 'medication'],
        patient_jwt
    )
    sats = process_satellites(data)
    dv = create_data_vault(sats)
    add_id_values(dv['links'])
    hub_equalizer(dv['hubs'])
    expected = {
        'satellites': {
            'ustan_sat_time_general_details': [
                {
                    'first_seen_date': '18/04/2017 00:00:00',
                    'dat_death': None,
                    'hub_time_id': 1
                }
            ],
            'ustan_sat_person_general_patient': [
                {
                    'name': 'HERMIONE KOCZUR',
                    'date_of_birth': '10/05/1954 00:00:00',
                    'dob': '10/05/1954 00:00:00',
                    'gender': 2,
                    'religion': 0,
                    'civil_st': 9,
                    'postcode': 'KY953HY',
                    'hub_person_id': 1
                }
            ],
            'ustan_sat_person_general_gp': [
                {
                    'hub_person_id': 1
                }
            ],
            'ustan_sat_location_general_details': [
                {
                    'ref_hospital': 617,
                    'hub_location_id': 1
                }
            ],
            'ustan_sat_event_general_details': [
                {
                    'smid': None,
                    'smid1': None,
                    'death_flag': 0,
                    'hub_event_id': 1
                }
            ],
            'ustan_sat_time_cycle_details': [
                {
                    'appointment_date': '13/09/2018 00:00:00',
                    'hub_time_id': 2
                },
                {
                    'appointment_date': '14/06/2018 00:00:00',
                    'hub_time_id': 3
                },
                {
                    'appointment_date': '20/06/2020 00:00:00',
                    'hub_time_id': 4
                },
                {
                    'appointment_date': '15/08/2020 00:00:00',
                    'hub_time_id': 5
                },
                {
                    'appointment_date': '02/09/2018 00:00:00',
                    'hub_time_id': 6
                },
                {
                    'appointment_date': '14/04/2019 00:00:00',
                    'hub_time_id': 7
                },
                {
                    'appointment_date': '26/03/2020 00:00:00',
                    'hub_time_id': 8
                },
                {
                    'appointment_date': '03/02/2021 00:00:00',
                    'hub_time_id': 9
                },
                {
                    'appointment_date': '22/04/2019 00:00:00',
                    'hub_time_id': 10
                },
                {
                    'appointment_date': '03/10/2020 00:00:00',
                    'hub_time_id': 11
                },
                {
                    'appointment_date': '14/11/2019 00:00:00',
                    'hub_time_id': 12
                },
                {
                    'appointment_date': '17/11/2019 00:00:00',
                    'hub_time_id': 13
                },
                {
                    'appointment_date': '06/08/2020 00:00:00',
                    'hub_time_id': 14
                },
                {
                    'appointment_date': '27/01/2021 00:00:00',
                    'hub_time_id': 15
                },
                {
                    'appointment_date': '29/10/2020 00:00:00',
                    'hub_time_id': 16
                },
                {
                    'appointment_date': '11/09/2018 00:00:00',
                    'hub_time_id': 17
                },
                {
                    'appointment_date': '02/01/2019 00:00:00',
                    'hub_time_id': 18
                },
                {
                    'appointment_date': '25/05/2019 00:00:00',
                    'hub_time_id': 19
                },
                {
                    'appointment_date': '22/03/2021 00:00:00',
                    'hub_time_id': 20
                },
                {
                    'appointment_date': '29/10/2020 00:00:00',
                    'hub_time_id': 21
                },
                {
                    'appointment_date': '06/03/2021 00:00:00',
                    'hub_time_id': 22
                },
                {
                    'appointment_date': '23/04/2018 00:00:00',
                    'hub_time_id': 23
                },
                {
                    'appointment_date': '10/01/2021 00:00:00',
                    'hub_time_id': 24
                }
            ],
            'ustan_sat_event_cycle_details': [
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX WKLY',
                    'cycle': 1,
                    'required_doses': 3649.93547,
                    'hub_event_id': 2
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D NEO (FEC)',
                    'cycle': 5,
                    'required_doses': 1685.106444,
                    'hub_event_id': 3
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (FEC)',
                    'cycle': 2,
                    'required_doses': 1893.169694,
                    'hub_event_id': 4
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (D)',
                    'cycle': 4,
                    'required_doses': 2266.419613,
                    'hub_event_id': 5
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D NEO (FEC)',
                    'cycle': 10,
                    'required_doses': 3925.381275,
                    'hub_event_id': 6
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D NEO (FEC)',
                    'cycle': 7,
                    'required_doses': 4852.662828,
                    'hub_event_id': 7
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 5,
                    'required_doses': 4882.554832,
                    'hub_event_id': 8
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 6,
                    'required_doses': 959.901679,
                    'hub_event_id': 9
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'VINORELBINE IV 1',
                    'cycle': 8,
                    'required_doses': 635.512842,
                    'hub_event_id': 10
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D NEO (FEC)',
                    'cycle': 1,
                    'required_doses': 1339.955771,
                    'hub_event_id': 11
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 8,
                    'required_doses': 1310.123773,
                    'hub_event_id': 12
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 7,
                    'required_doses': 3788.800093,
                    'hub_event_id': 13
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (D)',
                    'cycle': 1,
                    'required_doses': 3338.507707,
                    'hub_event_id': 14
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX WKLY',
                    'cycle': 3,
                    'required_doses': 918.45087,
                    'hub_event_id': 15
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX WKLY',
                    'cycle': 7,
                    'required_doses': 2004.030147,
                    'hub_event_id': 16
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (FEC)',
                    'cycle': 1,
                    'required_doses': 2037.483224,
                    'hub_event_id': 17
                },
                {
                    'drug_names': 'CAPOX',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (D)',
                    'cycle': 8,
                    'required_doses': 4984.528361,
                    'hub_event_id': 18
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX WKLY',
                    'cycle': 8,
                    'required_doses': 3828.312595,
                    'hub_event_id': 19
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 7,
                    'required_doses': 1290.775893,
                    'hub_event_id': 20
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'DOCETAXEL BREAST',
                    'cycle': 11,
                    'required_doses': 4094.76891,
                    'hub_event_id': 21
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'PACLITAX',
                    'cycle': 2,
                    'required_doses': 1560.428292,
                    'hub_event_id': 22
                },
                {
                    'drug_names': 'BEP 5 DAY MET',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'FEC-D (D)',
                    'cycle': 4,
                    'required_doses': 4536.198734,
                    'hub_event_id': 23
                },
                {
                    'drug_names': 'CARBO&PACLI WKLY',
                    'diagnosis': 'Breast Cancer',
                    'intention': 'Neo-Adjuvant',
                    'regime': 'DOCETAXEL BREAST',
                    'cycle': 14,
                    'required_doses': 2137.767392,
                    'hub_event_id': 24
                }
            ],
            'ustan_sat_time_intentions_details': [
                {
                    'init_appointment_date': '08/10/2020 00:00:00',
                    'appointment_date': '08/10/2020 00:00:00',
                    'hub_time_id': 25
                }
            ],
            'ustan_sat_person_intentions_details': [
                {
                    'hub_person_id': 3
                }
            ],
            'ustan_sat_event_intentions_details': [
                {
                    'intention_seq': 1,
                    'first_intention': 'Neo-Adjuvant',
                    'intention': 'Neo-Adjuvant',
                    'first_regime': 'FEC-D NEO (FEC)',
                    'hub_event_id': 25
                }
            ],
            'ustan_sat_time_regimes_details': [
                {
                    'init_appointment_date': '08/10/2020 00:00:00',
                    'appointment_date': '06/05/2021 00:00:00',
                    'hub_time_id': 26
                },
                {
                    'init_appointment_date': '08/10/2020 00:00:00',
                    'appointment_date': '02/12/2021 00:00:00',
                    'hub_time_id': 27
                },
                {
                    'init_appointment_date': '08/10/2020 00:00:00',
                    'appointment_date': '06/05/2021 00:00:00',
                    'hub_time_id': 28
                }
            ],
            'ustan_sat_event_regimes_details': [
                {
                    'regime_seq': 298,
                    'intention': 'Neo-Adjuvant',
                    'first_regime': 'FEC-D NEO (FEC)',
                    'regime': 'PACLITAX',
                    'hub_event_id': 26
                },
                {
                    'regime_seq': 1174,
                    'intention': 'Neo-Adjuvant',
                    'first_regime': 'FEC-D NEO (FEC)',
                    'regime': 'PACLITAX',
                    'hub_event_id': 27
                },
                {
                    'regime_seq': 1342,
                    'intention': 'Neo-Adjuvant',
                    'first_regime': 'FEC-D NEO (FEC)',
                    'regime': 'DOCETAXEL',
                    'hub_event_id': 28
                }
            ]
        },
        'hubs': {
            'hub_time': {
                'id': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28
                ],
                'chi': [
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224
                ]
            },
            'hub_person': {
                'id': [
                    1,
                    1,
                    3
                ],
                'chi': [
                    1005549224,
                    1005549224,
                    1005549224
                ]
            },
            'hub_object': {
                'id': []
            },
            'hub_location': {
                'id': [
                    1
                ],
                'chi': [
                    1005549224
                ]
            },
            'hub_event': {
                'id': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28
                ],
                'chi': [
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224,
                    1005549224
                ]
            }
        },
        'links': {
            'time_person_link': {
                'id': [
                    1,
                    2
                ],
                'time_id': [
                    1,
                    25
                ],
                'person_id': [
                    1,
                    3
                ]
            },
            'time_object_link': {
                'id': [],
                'time_id': [],
                'object_id': []
            },
            'time_location_link': {
                'id': [
                    1
                ],
                'time_id': [
                    1
                ],
                'location_id': [
                    1
                ]
            },
            'time_event_link': {
                'id': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28
                ],
                'time_id': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28
                ],
                'event_id': [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    28
                ]
            },
            'person_object_link': {
                'id': [],
                'person_id': [],
                'object_id': []
            },
            'person_location_link': {
                'id': [
                    1
                ],
                'person_id': [
                    1
                ],
                'location_id': [
                    1
                ]
            },
            'person_event_link': {
                'id': [
                    1,
                    2
                ],
                'person_id': [
                    1,
                    3
                ],
                'event_id': [
                    1,
                    25
                ]
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
                'id': [
                    1
                ],
                'location_id': [
                    1
                ],
                'event_id': [
                    1
                ]
            }
        }
    }
    assert dv == expected
