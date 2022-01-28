from components.jwt.validate import validate_jwt
import pytest

JWT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoi'\
      'YWNjZXNzIiwiZXhwIjoxNjQ1MzQ1MDczLCJqdGkiOiJjZTRlYjQ5NjQ2N'\
      'WY0ZmNhYTU4NzY1ZGI4NGRhMDIxNSIsInVzZXJJRCI6MTE3LCJpc3MiOi'\
      'JTZXJ1bXNBdXRoZW50aWNhdGlvbiIsImlhdCI6MTY0Mjc1MzA3Mywic3V'\
      'iIjoicHBwMUB1c3Rhbi5jb20iLCJncm91cElEcyI6WyJQQVRJRU5UIl0s'\
      'Im9yZ0lEIjoiVVNUQU4iLCJkZXB0SUQiOm51bGwsImRlcHROYW1lIjpud'\
      'WxsLCJzdGFmZklEIjpudWxsLCJuYW1lIjpudWxsLCJhdWQiOiJodHRwcz'\
      'ovL3NoY3Muc2VydW1zLmNzLnN0LWFuZHJld3MuYWMudWsvIn0.F6VexwH'\
      '5rUqrBs31Zm_QQwqCbGRWMK3dlk2gC31xhMU'


@pytest.mark.skip(reason="The JWT will be stop working")
def test_validation_validates_real_token():
    results = validate_jwt(JWT)
    expected_keys = [
        'serums_id',
        'hospital_id',
        'user_type',
        'status_code'
    ]
    assert expected_keys == list(dict.fromkeys(results))
    assert results['status_code'] == 200


@pytest.mark.skip(reason="The JWT will be stop working")
def test_validation_catches_malformed_token():
    results = validate_jwt(JWT[2:])
    assert results['status_code'] == 422
