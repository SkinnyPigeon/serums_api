from components.ml.data_for_ml import get_patient_data_for_ml


def test_can_get_patient_data():
    result = get_patient_data_for_ml(117)
    assert result[1] == 200
    assert len(result[0]) > 0


def test_can_handle_wrong_id():
    result = get_patient_data_for_ml(9898)
    assert result[1] == 500
    assert result[0] == {
        "message": "Patient not found with that Serums ID"
    }
