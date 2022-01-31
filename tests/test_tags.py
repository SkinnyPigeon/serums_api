from components.tags.tags import get_tags


def test_get_tags():
    result = get_tags('ustan')
    expected = {
        'tags': [
            'chemotherapy',
            'medication',
            'patient_appointments',
            'predictor',
            'treatment_outcome',
            'diagnostic',
            'patient_details',
            'wearable',
            'inpatient',
            'breast_cancer_information',
            'all'
        ],
        'translated': {
            'breast_cancer_information': {
                'translation': 'Breast Cancer Information'
            },
            'inpatient': {
                'translation': 'Inpatient'
            },
            'wearable': {
                'translation': 'Wearable'
            },
            'treatment_outcome': {
                'translation': 'Treatment Outcome'
            },
            'predictor': {
                'translation': 'Predictor'
            },
            'patient_appointments': {
                'translation': 'Patient Appointments'
            },
            'medication': {
                'translation': 'Medication'
            },
            'chemotherapy': {
                'translation': 'Chemotherapy'
            },
            'diagnostic': {
                'translation': 'Diagnostic'
            },
            'patient_details': {
                'translation': 'Patient details'
            },
            'all': {
                'translation': 'All'
            }
        }
    }
    assert result == expected
