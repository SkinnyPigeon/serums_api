from components.staff.verify_staff_member import check_staff_member
import pytest

right_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
            "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
            "joxNjQ3NTA1OTQ2LCJqdGkiOiIwZjFjZjk0Yz"\
            "NiMjg0NWE2ODc5ZGM4YTRjZWEwNmRkYiIsInV"\
            "zZXJJRCI6MjE2LCJpc3MiOiJTZXJ1bXNBdXRo"\
            "ZW50aWNhdGlvbiIsImlhdCI6MTY0NDkxMzk0N"\
            "iwic3ViIjoidGVzdG1lZGljYWxAdXN0YW4uY2"\
            "9tIiwiZ3JvdXBJRHMiOlsiTUVESUNBTF9TVEF"\
            "GRiJdLCJvcmdJRCI6IlVTVEFOIiwiZGVwdElE"\
            "IjpudWxsLCJkZXB0TmFtZSI6bnVsbCwic3RhZ"\
            "mZJRCI6bnVsbCwibmFtZSI6bnVsbCwiYXVkIj"\
            "oiaHR0cHM6Ly9zaGNzLnNlcnVtcy5jcy5zdC1"\
            "hbmRyZXdzLmFjLnVrLyJ9.VdceKMwPXWe7pH7"\
            "Ma2qAor2oeb02Uiz8m5uAZ_C8feE"

patient_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
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

wrong_id_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
               "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
               "joxNjQ1OTgwMDc2LCJqdGkiOiI1MjAyYWY5Yj"\
               "I0MDM0OTg0YWI0OTAxYTZlNjYwY2U4YSIsInV"\
               "zZXJJRCI6MTIwLCJpc3MiOiJTZXJ1bXNBdXRo"\
               "ZW50aWNhdGlvbiIsImlhdCI6MTY0MzM4ODA3N"\
               "iwic3ViIjoibWVkc3RhZmYxQHVzdGFuLmNvbS"\
               "IsImdyb3VwSURzIjpbIk1FRElDQUxfU1RBRkY"\
               "iXSwib3JnSUQiOiJVU1RBTiIsImRlcHRJRCI6"\
               "NCwiZGVwdE5hbWUiOiJNRURJQ0FMX1NUQUZGI"\
               "iwic3RhZmZJRCI6OTk5OSwibmFtZSI6IkNoYX"\
               "Jsb3R0ZSBXYXRzb24iLCJhdWQiOiJodHRwczo"\
               "vL3NoY3Muc2VydW1zLmNzLnN0LWFuZHJld3Mu"\
               "YWMudWsvIn0.vVHIlYeJFbxQCjvr4cRUrhrLs"\
               "25O6d1rjZBAL9bt4js"


# @pytest.mark.skip(reason="The JWTs will become invalid over time")
def test_should_validate_staff_member():
    results = check_staff_member(right_jwt)
    assert results is True


# @pytest.mark.skip(reason="The JWTs will become invalid over time")
def test_should_return_none_for_patient():
    results = check_staff_member(patient_jwt)
    assert results is False


# @pytest.mark.skip(reason="The JWTs will become invalid over time")
def test_should_return_none_for_wrong_staff_id():
    results = check_staff_member(wrong_id_jwt)
    assert results is False
