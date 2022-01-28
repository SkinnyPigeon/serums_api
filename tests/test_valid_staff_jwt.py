from components.staff.verify_staff_member import check_staff_member

right_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
            "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
            "joxNjQ1OTgwMDc2LCJqdGkiOiI1MjAyYWY5Yj"\
            "I0MDM0OTg0YWI0OTAxYTZlNjYwY2U4YSIsInV"\
            "zZXJJRCI6MTIwLCJpc3MiOiJTZXJ1bXNBdXRo"\
            "ZW50aWNhdGlvbiIsImlhdCI6MTY0MzM4ODA3N"\
            "iwic3ViIjoibWVkc3RhZmYxQHVzdGFuLmNvbS"\
            "IsImdyb3VwSURzIjpbIk1FRElDQUxfU1RBRkY"\
            "iXSwib3JnSUQiOiJVU1RBTiIsImRlcHRJRCI6"\
            "NCwiZGVwdE5hbWUiOiJNRURJQ0FMX1NUQUZGI"\
            "iwic3RhZmZJRCI6MTIwLCJuYW1lIjoiQ2hhcm"\
            "xvdHRlIFdhdHNvbiIsImF1ZCI6Imh0dHBzOi8"\
            "vc2hjcy5zZXJ1bXMuY3Muc3QtYW5kcmV3cy5h"\
            "Yy51ay8ifQ.eoCQlROTCsHGjuwGqKiP4kSQGy"\
            "3FCdoiraWOI782G2k"

patient_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."\
              "eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwI"\
              "joxNjQ1OTgwMDc2LCJqdGkiOiI1MjAyYWY5Yj"\
              "I0MDM0OTg0YWI0OTAxYTZlNjYwY2U4YSIsInV"\
              "zZXJJRCI6MTIwLCJpc3MiOiJTZXJ1bXNBdXRo"\
              "ZW50aWNhdGlvbiIsImlhdCI6MTY0MzM4ODA3N"\
              "iwic3ViIjoibWVkc3RhZmYxQHVzdGFuLmNvbS"\
              "IsImdyb3VwSURzIjpbIlBBVElFTlQiXSwib3J"\
              "nSUQiOiJVU1RBTiIsImRlcHRJRCI6NCwiZGVw"\
              "dE5hbWUiOiJNRURJQ0FMX1NUQUZGIiwic3RhZ"\
              "mZJRCI6MTIwLCJuYW1lIjoiQ2hhcmxvdHRlIF"\
              "dhdHNvbiIsImF1ZCI6Imh0dHBzOi8vc2hjcy5"\
              "zZXJ1bXMuY3Muc3QtYW5kcmV3cy5hYy51ay8i"\
              "fQ.HoL_D_Lf2lyCz7YCuWKTkQf_sk2Mt_v7W9"\
              "gO_v0LTQ0"

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


def test_should_validate_staff_member():
    results = check_staff_member(right_jwt)
    expected_keys = ['id', 'department_id']
    assert type(results) == dict
    assert list(dict.fromkeys(results)) == expected_keys


def test_should_return_none_for_patient():
    results = check_staff_member(patient_jwt)
    assert results is None


def test_should_return_none_for_wrong_staff_id():
    results = check_staff_member(wrong_id_jwt)
    assert results is None
