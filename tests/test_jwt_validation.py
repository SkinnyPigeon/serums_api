from components.jwt.validate import validate_jwt
import pytest

JWT = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
      "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
      "joxNjQ3NTA1NjYxLCJqdGkiOiI0ZWUyZGY3Zm"\
      "Y3NTk0MDg1YmE5NjUyYzdkMmQ2M2FlMiIsInV"\
      "zZXJJRCI6MjE1LCJpc3MiOiJTZXJ1bXNBdXRo"\
      "ZW50aWNhdGlvbiIsImlhdCI6MTY0NDkxMzY2M"\
      "Swic3ViIjoidGVzdHBhdGllbnRAdXN0YW4uY2"\
      "9tIiwiZ3JvdXBJRHMiOlsiUEFUSUVOVCJdLCJ"\
      "vcmdJRCI6IlVTVEFOIiwiZGVwdElEIjpudWxs"\
      "LCJkZXB0TmFtZSI6bnVsbCwic3RhZmZJRCI6b"\
      "nVsbCwibmFtZSI6bnVsbCwiYXVkIjoiaHR0cH"\
      "M6Ly9zaGNzLnNlcnVtcy5jcy5zdC1hbmRyZXd"\
      "zLmFjLnVrLyJ9.brv3p2nUZZ9OPwlBeVTnLGb"\
      "whJ620hYkpog5jqObRP8"


# @pytest.mark.skip(reason="The JWT will be stop working")
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


# @pytest.mark.skip(reason="The JWT will be stop working")
def test_validation_catches_malformed_token():
    results = validate_jwt(JWT[2:])
    assert results['status_code'] == 422
