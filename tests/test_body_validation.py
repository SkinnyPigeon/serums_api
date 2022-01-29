from components.validation.body import validate_body

public_key = "-----BEGIN PUBLIC KEY-----\n"\
             "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB"\
             "iQKBgQCLCWYFVX0YmP4Hezn7fOdTFiuO\n"\
             "41c8ZLLpN0jCAZjLPCi6ZFN1nhaXn9Hu"\
             "CJFIYimPDC04u1VJclD5GfVE6zuDRUcq\n"\
             "tVDQP/Qw88WKpDY4e2zjIddIC0Qs9uE1"\
             "ErX7ae+yQE8vXf0OTrBZQRyCH7DtM4/e\n"\
             "pAJ84ck6ySK3CIwF0QIDAQAB\n"\
             "-----END PUBLIC KEY-----"

bad_public_key = "-----BEGIN PUBLIC KEY-----\n"\
                 "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCB"\
                 "CJFIYimPDC04u1VJclD5GfVE6zuDRUcq\n"\
                 "tVDQP/Qw88WKpDY4e2zjIddIC0Qs9uE1"\
                 "ErX7ae+yQE8vXf0OTrBZQRyCH7DtM4/e\n"\
                 "pAJ84ck6ySK3CIwF0QIDAQAB\n"\
                 "-----END PUBLIC KEY-----"


def test_can_spot_missing_fields():
    body = {
        'tags': ['a', 'b', 'c'],
        'serums_id': 123
    }
    unencrypted = validate_body(body)
    encrypted = validate_body(body, encrypted=True)
    assert len(unencrypted) == 1
    assert len(encrypted) == 2
    assert unencrypted[0] == "Missing required field: HOSPITAL_IDS"
    assert "Missing required field: PUBLIC_KEY" in encrypted


def test_can_spot_incorrectly_formatted_key():
    body = {
        'tags': ['a', 'b', 'c'],
        'serums_id': 123,
        'hospital_ids': ['ustan'],
        'public_key': 'abc'
    }
    result = validate_body(body, encrypted=True)
    assert result == ['Public key incorrectly formatted']
    body['public_key'] = bad_public_key
    assert result == ['Public key incorrectly formatted']


def test_can_validate_properly_formatted_request():
    body = {
        'tags': ['a', 'b', 'c'],
        'serums_id': 123,
        'hospital_ids': ['ustan'],
        'public_key': public_key
    }
    result = validate_body(body, encrypted=True)
    assert len(result) == 0


def test_can_spot_bad_data_types():
    body = {
        'tags': ['a', 'b', 'c'],
        'serums_id': '123',
        'hospital_ids': ['ustan']
    }
    result = validate_body(body)
    assert len(result) == 1
    assert result[0] == "Incorrect data type for SERUMS_ID. "\
                        "Expected <class 'int'>. "\
                        "Received <class 'str'>"