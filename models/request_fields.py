from typing import Optional
from pydantic import BaseModel
from datetime import datetime
import json


class HelloResponse(BaseModel):
    __root__: dict = {"hello": "Welcome to the API. The server is on"}


class StaffMemberDepartmentResponse(BaseModel):
    serums_id: int = 120
    staff_id: int = 120
    name: str = "Charlotte Watson"
    department_id: int = 4
    department_name: str = "MEDICAL_STAFF"


class FullDepartmentRequest(BaseModel):
    hospital_id: str = 'USTAN'


staff_details = json.loads('''
    [
        {
            "serums_id": 364,
            "staff_id": 6000,
            "name": "Isla MacDonald",
            "department_id": 1,
            "department_name": "Emergency"
        },
        {
            "serums_id": 391,
            "staff_id": 6001,
            "name": "Charles Stewart",
            "department_id": 1,
            "department_name": "Emergency"
        },
        {
            "serums_id": 390,
            "staff_id": 6002,
            "name": "Oliver Wilson",
            "department_id": 3,
            "department_name": "Consultant"
        }
    ]
''')


class FullDepartmentResponse(BaseModel):
    __root__: list[dict] = staff_details


class SingleHospitalTagsRequest(BaseModel):
    hospital_id: str = 'USTAN'


class SingleHospitalTagsResponse(BaseModel):
    tags: list[str] = ["chemotherapy",
                       "medication",
                       "patient_appointments",
                       "predictor",
                       "treatment_outcome",
                       "diagnostic",
                       "patient_details",
                       "wearable",
                       "inpatient",
                       "breast_cancer_information",
                       "all"]
    translated: dict = {
        "breast_cancer_information": {
            "translation": "Breast Cancer Information"
        },
        "inpatient": {
            "translation": "Inpatient"
        },
        "wearable": {
            "translation": "Wearable"
        },
        "treatment_outcome": {
            "translation": "Treatment Outcome"
        },
        "predictor": {
            "translation": "Predictor"
        },
        "patient_appointments": {
            "translation": "Patient Appointments"
        },
        "medication": {
            "translation": "Medication"
        },
        "chemotherapy": {
            "translation": "Chemotherapy"
        },
        "diagnostic": {
            "translation": "Diagnostic"
        },
        "patient_details": {
            "translation": "Patient details"
        },
        "all": {
            "translation": "All"
        }
    }


class MultiHospitalTagsRequest(BaseModel):
    hospital_ids: list = [
        "USTAN",
        "FCRB",
        "ZMC"
    ]


class MultiHospitalTagsResponse(BaseModel):
    USTAN: dict = {
        "tags": [
            "chemotherapy",
            "medication",
            "patient_appointments",
            "predictor",
            "treatment_outcome",
            "diagnostic",
            "patient_details",
            "wearable",
            "inpatient",
            "breast_cancer_information",
            "all"
        ],
        "translated": {
            "breast_cancer_information": {
                "translation": "Breast Cancer Information"
            },
            "inpatient": {
                "translation": "Inpatient"
            },
            "wearable": {
                "translation": "Wearable"
            },
            "treatment_outcome": {
                "translation": "Treatment Outcome"
            },
            "predictor": {
                "translation": "Predictor"
            },
            "patient_appointments": {
                "translation": "Patient Appointments"
            },
            "medication": {
                "translation": "Medication"
            },
            "chemotherapy": {
                "translation": "Chemotherapy"
            },
            "diagnostic": {
                "translation": "Diagnostic"
            },
            "patient_details": {
                "translation": "Patient details"
            },
            "all": {
                "translation": "All"
            }
        }
    }
    FCRB: dict = {
        "tags": [
            "diagnostic",
            "patient_details",
            "healthcare_providers",
            "patient_appointments",
            "treatments",
            "medication",
            "documents",
            "additional_information",
            "wearable",
            "patient_address",
            "personal",
            "all"
        ],
        "translated": {
            "additional_information": {
                "translation": "Información Adicional"
            },
            "documents": {
                "translation": "Documentos"
            },
            "wearable": {
                "translation": "Portable"
            },
            "diagnostic": {
                "translation": "Diagnòstic"
            },
            "medication": {
                "translation": "Medicació"
            },
            "patient_details": {
                "translation": "Detalls de Pacient"
            },
            "patient_address": {
                "translation": "Adreça de pacient"
            },
            "patient_appointments": {
                "translation": "Cites"
            },
            "healthcare_providers": {
                "translation": "Proveïdors de Salut"
            },
            "treatments": {
                "translation": "Tractaments"
            },
            "personal": {
                "translation": "Personal"
            },
            "all": {
                "translation": "Tots"
            }
        }
    },
    ZMC: dict = {
        "tags": [
            "wearable",
            "diagnostic",
            "medication",
            "operations",
            "documents",
            "treatments",
            "healthcare_providers",
            "allergies",
            "personal",
            "patient_appointments",
            "drugs_and_alcohol",
            "all"
        ],
        "translated": {
            "healthcare_providers": {
                "translation": "Zorgverlener"
            },
            "medication": {
                "translation": "Medicatie"
            },
            "wearable": {
                "translation": "Wearable/Sensor"
            },
            "diagnostic": {
                "translation": "Diagnostiek"
            },
            "patient_details": {
                "translation": "Patiënten informatie"
            },
            "patient_address": {
                "translation": "Adres van de patiënt"
            },
            "patient_appointments": {
                "translation": "Afspraken"
            },
            "operations": {
                "translation": "Operaties"
            },
            "documents": {
                "translation": "Documenten"
            },
            "drugs_and_alcohol": {
                "translation": "Drugs en alcohol"
            },
            "allergies": {
                "translation": "Allergieën"
            },
            "additional_information": {
                "translation": "Additionele informatie"
            },
            "treatments": {
                "translation": "Behandelingen"
            },
            "personal": {
                "translation": "Persoonlijke informatie"
            },
            "all": {
                "translation": "Alle"
            }
        }
    }


class NotAuthenticated(BaseModel):
    message: str = "Not authenticated"


class AddUserRequest(BaseModel):
    serums_id: int = 26537
    patient_id: int = 1923892
    hospital_id: str = 'USTAN'


class HandleError500(BaseModel):
    message: str


class AddUserSuccessResponse(BaseModel):
    message: str = "User added correctly"


class UnauthorizedResponse(BaseModel):
    message: str


class AddUserUnauthorizedResponse(BaseModel):
    message: str = "Only admins can add users"


class RemoveUserRequest(BaseModel):
    serums_id: int = 26537
    hospital_ids: list = [
        "USTAN",
        "FCRB",
        "ZMC"
    ]


removed_user = json.loads('''
    {
        "ustan": {
            "message": "User successfully removed from USTAN"
        },
        "fcrb": {
            "message": "User not found in FCRB"
        }
    }
''')


class RemoveUserSuccessResponse(BaseModel):
    __root__: dict = removed_user


class RemoveUserUnauthorizedResponse(BaseModel):
    message: str


machine_learning = json.loads('''
    {
        "cycles": {
            "0": {
            "id": 1,
            "chi": 1005549224,
            "regime_id": 1,
            "intention_id": 1,
            "cycle_id": 1,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-09-13",
            "elapsed_days": 0,
            "interval_days": 20,
            "appointment_date": "2018-09-13",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX WKLY",
            "p_ps": -1,
            "ps": 2,
            "nausea": 3,
            "vomiting": 0,
            "diarrhoea": 2,
            "constipation": 1,
            "oralMucositis": 0,
            "oesophagitis": 4,
            "cycle": 1,
            "neurotoxicity": 4,
            "handFoot": 3,
            "skin": 3,
            "hypersensitivity": 4,
            "fatigue": 5,
            "required_doses": 3649.93547
            },
            "1": {
            "id": 1124,
            "chi": 1005549224,
            "regime_id": 130,
            "intention_id": 88,
            "cycle_id": 1124,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-03-22",
            "elapsed_days": 84,
            "interval_days": 20,
            "appointment_date": "2018-06-14",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D NEO (FEC)",
            "p_ps": -1,
            "ps": 1,
            "nausea": 1,
            "vomiting": 4,
            "diarrhoea": 4,
            "constipation": 6,
            "oralMucositis": 0,
            "oesophagitis": 1,
            "cycle": 5,
            "neurotoxicity": 5,
            "handFoot": 3,
            "skin": 2,
            "hypersensitivity": 5,
            "fatigue": 5,
            "required_doses": 1685.106444
            },
            "2": {
            "id": 7336,
            "chi": 1005549224,
            "regime_id": 884,
            "intention_id": 523,
            "cycle_id": 7336,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-05-30",
            "elapsed_days": 21,
            "interval_days": 20,
            "appointment_date": "2020-06-20",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (FEC)",
            "p_ps": -1,
            "ps": 1,
            "nausea": 1,
            "vomiting": 0,
            "diarrhoea": 3,
            "constipation": 2,
            "oralMucositis": 1,
            "oesophagitis": 5,
            "cycle": 2,
            "neurotoxicity": 5,
            "handFoot": 5,
            "skin": 1,
            "hypersensitivity": 4,
            "fatigue": 5,
            "required_doses": 1893.169694
            },
            "3": {
            "id": 13762,
            "chi": 1005549224,
            "regime_id": 1644,
            "intention_id": 982,
            "cycle_id": 13762,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-06-13",
            "elapsed_days": 63,
            "interval_days": 19,
            "appointment_date": "2020-08-15",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (D)",
            "p_ps": -1,
            "ps": 1,
            "nausea": 1,
            "vomiting": 0,
            "diarrhoea": 4,
            "constipation": 6,
            "oralMucositis": 1,
            "oesophagitis": 4,
            "cycle": 4,
            "neurotoxicity": 4,
            "handFoot": 2,
            "skin": 1,
            "hypersensitivity": 5,
            "fatigue": 3,
            "required_doses": 2266.419613
            },
            "4": {
            "id": 15217,
            "chi": 1005549224,
            "regime_id": 1797,
            "intention_id": 1064,
            "cycle_id": 15217,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-02-25",
            "elapsed_days": 189,
            "interval_days": 18,
            "appointment_date": "2018-09-02",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D NEO (FEC)",
            "p_ps": -1,
            "ps": 3,
            "nausea": 2,
            "vomiting": 3,
            "diarrhoea": 5,
            "constipation": 3,
            "oralMucositis": 1,
            "oesophagitis": 1,
            "cycle": 10,
            "neurotoxicity": 2,
            "handFoot": 2,
            "skin": 1,
            "hypersensitivity": 2,
            "fatigue": 5,
            "required_doses": 3925.381275
            },
            "5": {
            "id": 15490,
            "chi": 1005549224,
            "regime_id": 1834,
            "intention_id": 1087,
            "cycle_id": 15490,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-12-09",
            "elapsed_days": 126,
            "interval_days": 18,
            "appointment_date": "2019-04-14",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D NEO (FEC)",
            "p_ps": -1,
            "ps": 3,
            "nausea": 2,
            "vomiting": 2,
            "diarrhoea": 2,
            "constipation": 4,
            "oralMucositis": 3,
            "oesophagitis": 6,
            "cycle": 7,
            "neurotoxicity": 5,
            "handFoot": 2,
            "skin": 6,
            "hypersensitivity": 1,
            "fatigue": 5,
            "required_doses": 4852.662828
            },
            "6": {
            "id": 15878,
            "chi": 1005549224,
            "regime_id": 1888,
            "intention_id": 1110,
            "cycle_id": 15878,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-01-02",
            "elapsed_days": 84,
            "interval_days": 21,
            "appointment_date": "2020-03-26",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 1,
            "nausea": 1,
            "vomiting": 2,
            "diarrhoea": 3,
            "constipation": 1,
            "oralMucositis": 1,
            "oesophagitis": 6,
            "cycle": 5,
            "neurotoxicity": 6,
            "handFoot": 4,
            "skin": 2,
            "hypersensitivity": 4,
            "fatigue": 5,
            "required_doses": 4882.554832
            },
            "7": {
            "id": 16393,
            "chi": 1005549224,
            "regime_id": 1939,
            "intention_id": 1142,
            "cycle_id": 16393,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-10-21",
            "elapsed_days": 105,
            "interval_days": 15,
            "appointment_date": "2021-02-03",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 1,
            "nausea": 2,
            "vomiting": 4,
            "diarrhoea": 5,
            "constipation": 3,
            "oralMucositis": 1,
            "oesophagitis": 6,
            "cycle": 6,
            "neurotoxicity": 1,
            "handFoot": 4,
            "skin": 1,
            "hypersensitivity": 3,
            "fatigue": 6,
            "required_doses": 959.901679
            },
            "8": {
            "id": 18326,
            "chi": 1005549224,
            "regime_id": 2172,
            "intention_id": 1294,
            "cycle_id": 18326,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-11-26",
            "elapsed_days": 147,
            "interval_days": 18,
            "appointment_date": "2019-04-22",
            "intention": "Neo-Adjuvant",
            "regime": "VINORELBINE IV 1",
            "p_ps": -1,
            "ps": 1,
            "nausea": 3,
            "vomiting": 3,
            "diarrhoea": 5,
            "constipation": 6,
            "oralMucositis": 0,
            "oesophagitis": 3,
            "cycle": 8,
            "neurotoxicity": 1,
            "handFoot": 6,
            "skin": 6,
            "hypersensitivity": 5,
            "fatigue": 2,
            "required_doses": 635.512842
            },
            "9": {
            "id": 19636,
            "chi": 1005549224,
            "regime_id": 2349,
            "intention_id": 1396,
            "cycle_id": 19636,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-10-03",
            "elapsed_days": 0,
            "interval_days": 16,
            "appointment_date": "2020-10-03",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D NEO (FEC)",
            "p_ps": -1,
            "ps": 2,
            "nausea": 1,
            "vomiting": 1,
            "diarrhoea": 4,
            "constipation": 6,
            "oralMucositis": 0,
            "oesophagitis": 4,
            "cycle": 1,
            "neurotoxicity": 1,
            "handFoot": 5,
            "skin": 1,
            "hypersensitivity": 5,
            "fatigue": 4,
            "required_doses": 1339.955771
            },
            "10": {
            "id": 20702,
            "chi": 1005549224,
            "regime_id": 2457,
            "intention_id": 1456,
            "cycle_id": 20702,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2019-06-20",
            "elapsed_days": 147,
            "interval_days": 17,
            "appointment_date": "2019-11-14",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 3,
            "nausea": 0,
            "vomiting": 0,
            "diarrhoea": 6,
            "constipation": 1,
            "oralMucositis": 1,
            "oesophagitis": 6,
            "cycle": 8,
            "neurotoxicity": 4,
            "handFoot": 6,
            "skin": 3,
            "hypersensitivity": 1,
            "fatigue": 6,
            "required_doses": 1310.123773
            },
            "11": {
            "id": 21555,
            "chi": 1005549224,
            "regime_id": 2564,
            "intention_id": 1512,
            "cycle_id": 21555,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2019-07-14",
            "elapsed_days": 126,
            "interval_days": 20,
            "appointment_date": "2019-11-17",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 2,
            "nausea": 2,
            "vomiting": 0,
            "diarrhoea": 3,
            "constipation": 1,
            "oralMucositis": 2,
            "oesophagitis": 3,
            "cycle": 7,
            "neurotoxicity": 4,
            "handFoot": 5,
            "skin": 5,
            "hypersensitivity": 2,
            "fatigue": 6,
            "required_doses": 3788.800093
            },
            "12": {
            "id": 24182,
            "chi": 1005549224,
            "regime_id": 2891,
            "intention_id": 1710,
            "cycle_id": 24182,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-08-06",
            "elapsed_days": 0,
            "interval_days": 15,
            "appointment_date": "2020-08-06",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (D)",
            "p_ps": -1,
            "ps": 2,
            "nausea": 2,
            "vomiting": 3,
            "diarrhoea": 6,
            "constipation": 2,
            "oralMucositis": 3,
            "oesophagitis": 3,
            "cycle": 1,
            "neurotoxicity": 2,
            "handFoot": 2,
            "skin": 5,
            "hypersensitivity": 4,
            "fatigue": 4,
            "required_doses": 3338.507707
            },
            "13": {
            "id": 28527,
            "chi": 1005549224,
            "regime_id": 3423,
            "intention_id": 2032,
            "cycle_id": 28527,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-12-16",
            "elapsed_days": 42,
            "interval_days": 20,
            "appointment_date": "2021-01-27",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX WKLY",
            "p_ps": -1,
            "ps": 1,
            "nausea": 2,
            "vomiting": 1,
            "diarrhoea": 1,
            "constipation": 6,
            "oralMucositis": 2,
            "oesophagitis": 6,
            "cycle": 3,
            "neurotoxicity": 6,
            "handFoot": 1,
            "skin": 2,
            "hypersensitivity": 1,
            "fatigue": 1,
            "required_doses": 918.45087
            },
            "14": {
            "id": 28589,
            "chi": 1005549224,
            "regime_id": 3421,
            "intention_id": 2030,
            "cycle_id": 28589,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-06-25",
            "elapsed_days": 126,
            "interval_days": 15,
            "appointment_date": "2020-10-29",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX WKLY",
            "p_ps": -1,
            "ps": 2,
            "nausea": 0,
            "vomiting": 2,
            "diarrhoea": 2,
            "constipation": 3,
            "oralMucositis": 3,
            "oesophagitis": 2,
            "cycle": 7,
            "neurotoxicity": 3,
            "handFoot": 6,
            "skin": 3,
            "hypersensitivity": 5,
            "fatigue": 3,
            "required_doses": 2004.030147
            },
            "15": {
            "id": 30524,
            "chi": 1005549224,
            "regime_id": 3647,
            "intention_id": 2161,
            "cycle_id": 30524,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-09-11",
            "elapsed_days": 0,
            "interval_days": 16,
            "appointment_date": "2018-09-11",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (FEC)",
            "p_ps": -1,
            "ps": 3,
            "nausea": 0,
            "vomiting": 1,
            "diarrhoea": 6,
            "constipation": 6,
            "oralMucositis": 3,
            "oesophagitis": 1,
            "cycle": 1,
            "neurotoxicity": 1,
            "handFoot": 4,
            "skin": 1,
            "hypersensitivity": 2,
            "fatigue": 1,
            "required_doses": 2037.483224
            },
            "16": {
            "id": 38255,
            "chi": 1005549224,
            "regime_id": 4544,
            "intention_id": 2679,
            "cycle_id": 38255,
            "drug_names": "CAPOX",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-08-08",
            "elapsed_days": 147,
            "interval_days": 15,
            "appointment_date": "2019-01-02",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (D)",
            "p_ps": -1,
            "ps": 1,
            "nausea": 0,
            "vomiting": 0,
            "diarrhoea": 2,
            "constipation": 6,
            "oralMucositis": 0,
            "oesophagitis": 2,
            "cycle": 8,
            "neurotoxicity": 4,
            "handFoot": 5,
            "skin": 2,
            "hypersensitivity": 4,
            "fatigue": 4,
            "required_doses": 4984.528361
            },
            "17": {
            "id": 38391,
            "chi": 1005549224,
            "regime_id": 4555,
            "intention_id": 2685,
            "cycle_id": 38391,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-12-29",
            "elapsed_days": 147,
            "interval_days": 15,
            "appointment_date": "2019-05-25",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX WKLY",
            "p_ps": -1,
            "ps": 2,
            "nausea": 1,
            "vomiting": 4,
            "diarrhoea": 2,
            "constipation": 1,
            "oralMucositis": 3,
            "oesophagitis": 1,
            "cycle": 8,
            "neurotoxicity": 2,
            "handFoot": 6,
            "skin": 4,
            "hypersensitivity": 5,
            "fatigue": 1,
            "required_doses": 3828.312595
            },
            "18": {
            "id": 39699,
            "chi": 1005549224,
            "regime_id": 4705,
            "intention_id": 2766,
            "cycle_id": 39699,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-11-16",
            "elapsed_days": 126,
            "interval_days": 15,
            "appointment_date": "2021-03-22",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 3,
            "nausea": 0,
            "vomiting": 1,
            "diarrhoea": 5,
            "constipation": 5,
            "oralMucositis": 0,
            "oesophagitis": 3,
            "cycle": 7,
            "neurotoxicity": 5,
            "handFoot": 6,
            "skin": 6,
            "hypersensitivity": 6,
            "fatigue": 3,
            "required_doses": 1290.775893
            },
            "19": {
            "id": 40280,
            "chi": 1005549224,
            "regime_id": 4773,
            "intention_id": 2814,
            "cycle_id": 40280,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-04-02",
            "elapsed_days": 210,
            "interval_days": 20,
            "appointment_date": "2020-10-29",
            "intention": "Neo-Adjuvant",
            "regime": "DOCETAXEL BREAST",
            "p_ps": -1,
            "ps": 1,
            "nausea": 3,
            "vomiting": 4,
            "diarrhoea": 4,
            "constipation": 5,
            "oralMucositis": 0,
            "oesophagitis": 3,
            "cycle": 11,
            "neurotoxicity": 4,
            "handFoot": 4,
            "skin": 4,
            "hypersensitivity": 1,
            "fatigue": 2,
            "required_doses": 4094.76891
            },
            "20": {
            "id": 40288,
            "chi": 1005549224,
            "regime_id": 4798,
            "intention_id": 2798,
            "cycle_id": 40288,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2021-02-13",
            "elapsed_days": 21,
            "interval_days": 15,
            "appointment_date": "2021-03-06",
            "intention": "Neo-Adjuvant",
            "regime": "PACLITAX",
            "p_ps": -1,
            "ps": 2,
            "nausea": 4,
            "vomiting": 4,
            "diarrhoea": 1,
            "constipation": 1,
            "oralMucositis": 0,
            "oesophagitis": 3,
            "cycle": 2,
            "neurotoxicity": 3,
            "handFoot": 3,
            "skin": 1,
            "hypersensitivity": 3,
            "fatigue": 2,
            "required_doses": 1560.428292
            },
            "21": {
            "id": 42778,
            "chi": 1005549224,
            "regime_id": 5092,
            "intention_id": 3007,
            "cycle_id": 42778,
            "drug_names": "BEP 5 DAY MET",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2018-02-19",
            "elapsed_days": 63,
            "interval_days": 19,
            "appointment_date": "2018-04-23",
            "intention": "Neo-Adjuvant",
            "regime": "FEC-D (D)",
            "p_ps": -1,
            "ps": 3,
            "nausea": 2,
            "vomiting": 2,
            "diarrhoea": 5,
            "constipation": 2,
            "oralMucositis": 3,
            "oesophagitis": 5,
            "cycle": 4,
            "neurotoxicity": 3,
            "handFoot": 6,
            "skin": 6,
            "hypersensitivity": 4,
            "fatigue": 6,
            "required_doses": 4536.198734
            },
            "22": {
            "id": 42903,
            "chi": 1005549224,
            "regime_id": 5084,
            "intention_id": 3005,
            "cycle_id": 42903,
            "drug_names": "CARBO&PACLI WKLY",
            "diagnosis": "Breast Cancer",
            "init_appointment_date": "2020-04-12",
            "elapsed_days": 273,
            "interval_days": 17,
            "appointment_date": "2021-01-10",
            "intention": "Neo-Adjuvant",
            "regime": "DOCETAXEL BREAST",
            "p_ps": -1,
            "ps": 3,
            "nausea": 4,
            "vomiting": 1,
            "diarrhoea": 5,
            "constipation": 4,
            "oralMucositis": 3,
            "oesophagitis": 4,
            "cycle": 14,
            "neurotoxicity": 4,
            "handFoot": 1,
            "skin": 3,
            "hypersensitivity": 4,
            "fatigue": 1,
            "required_doses": 2137.767392
            }
        },
        "general": {
            "0": {
            "id": 336,
            "chi": 1005549224,
            "incidence_date": "2017-04-18",
            "site_icd_10": "C50.9",
            "name": "HERMIONE KOCZUR",
            "date_of_birth": "1954-05-10",
            "first_seen_date": "2017-04-18",
            "site": "C50.9",
            "histology": 8508,
            "primary": 1,
            "metastasis1": "C00.0",
            "metastasis2": "None",
            "metastasis3": "None",
            "smid": "None",
            "smid1": "None",
            "cong_heart_fail_flag": 0,
            "con_tiss_disease_rheum_flag": 0,
            "dementia_flag": 0,
            "pulmonary_flag": 0,
            "con_tiss_flag": 0,
            "diabetes_flag": 0,
            "para_hemiplegia_flag": 0,
            "renal_flag": 0,
            "liver_flag": 0,
            "aids_hiv_flag": 0,
            "cancer_flag": 6,
            "charlson_score": 6,
            "dob": "1954-05-10",
            "age": 63,
            "simd": 5,
            "simd1": 1,
            "side": 2,
            "gender": 2,
            "age_at_diagnosis": 5.2,
            "weight": 68.6,
            "bmi": 25.5,
            "height": 1.64,
            "religion": 0,
            "civil_st": 9,
            "ref_hospital": 617,
            "postcode_pre": "KY",
            "postcode_suf": "953HY",
            "stage": 2,
            "stage_detail": "2A",
            "tnm_t": 1,
            "tnm_t_detail": 1,
            "tnm_n": 0,
            "tnm_n_detail": 0,
            "tnm_m": 0,
            "perf_stat": "None",
            "smr01_flag": 0,
            "postcode": "KY953HY",
            "gp_name": "KIVIOJA",
            "death_flag": 0,
            "survival_days": "None",
            "dat_death": "None",
            "gp_id": 18
            }
        },
        "intentions": {
            "0": {
            "id": 345,
            "chi": 1005549224,
            "patient_id": 335,
            "intention_id": 344,
            "intention_seq": 1,
            "first_intention": "Neo-Adjuvant",
            "regime_ratio": 1,
            "cycle_ratio": 13,
            "intention": "Neo-Adjuvant",
            "first_regime": "FEC-D NEO (FEC)",
            "init_appointment_date": "2020-10-08",
            "elapsed_days": 0,
            "appointment_date": "2020-10-08"
            }
        },
        "patients": {
            "0": {
            "id": 336,
            "chi": 1005549224,
            "patient_id": 335,
            "first_intention": "Neo-Adjuvant",
            "appointment_date": "2020-10-08"
            }
        },
        "regimes": {
            "0": {
            "id": 1151,
            "chi": 1005549224,
            "intention_id": 670,
            "regime_id": 1151,
            "regime_seq": 298,
            "regime_ratio": "None",
            "cycle_ratio": 13,
            "intention": "Neo-Adjuvant",
            "prev_regime": "EPI/CYCLO MET",
            "first_regime": "FEC-D NEO (FEC)",
            "regime": "PACLITAX",
            "interval_days": 20,
            "elapsed_days": 210,
            "init_appointment_date": "2020-10-08",
            "appointment_date": "2021-05-06"
            },
            "1": {
            "id": 4515,
            "chi": 1005549224,
            "intention_id": 2642,
            "regime_id": 4515,
            "regime_seq": 1174,
            "regime_ratio": "None",
            "cycle_ratio": 13,
            "intention": "Neo-Adjuvant",
            "prev_regime": "PACLITAX",
            "first_regime": "FEC-D NEO (FEC)",
            "regime": "PACLITAX",
            "interval_days": 20,
            "elapsed_days": 420,
            "init_appointment_date": "2020-10-08",
            "appointment_date": "2021-12-02"
            },
            "2": {
            "id": 5184,
            "chi": 1005549224,
            "intention_id": 3055,
            "regime_id": 5184,
            "regime_seq": 1342,
            "regime_ratio": "None",
            "cycle_ratio": 13,
            "intention": "Neo-Adjuvant",
            "prev_regime": "FEC-D NEO (FEC)",
            "first_regime": "FEC-D NEO (FEC)",
            "regime": "DOCETAXEL",
            "interval_days": 17,
            "elapsed_days": 210,
            "init_appointment_date": "2020-10-08",
            "appointment_date": "2021-05-06"
            }
        },
        "smr01": {
            "0": {
            "id": 14,
            "chi": 1005549224,
            "incidence_date": "2016-04-30",
            "admission_date": "2016-06-02",
            "length_of_stay": 0,
            "other_condition1": "None",
            "other_condition2": "None",
            "other_condition3": "None",
            "main_operation_b": "Z94.3",
            "discharge_date": "2016-06-01",
            "waiting_list_type": 2,
            "main_condition": "C509",
            "main_operation_a": "X388",
            "marital_status": "Z",
            "ethnic_group": "98"
            },
            "1": {
            "id": 33,
            "chi": 1005549224,
            "incidence_date": "2016-04-30",
            "admission_date": "2016-09-16",
            "length_of_stay": 0,
            "other_condition1": "C773",
            "other_condition2": "None",
            "other_condition3": "None",
            "main_operation_b": "None",
            "discharge_date": "2016-09-15",
            "waiting_list_type": 2,
            "main_condition": "C509",
            "main_operation_a": "X369",
            "marital_status": "Z",
            "ethnic_group": "1B"
            }
        },
        "smr06": {
            "0": {
            "id": 581,
            "chi": 1005549224,
            "incidence_date": "2015-03-04",
            "er_status": 1,
            "her2_status": 1,
            "stage_clinical_t": "4b",
            "stage_clinical_n": 1,
            "stage_clinical_m": "X",
            "num_positive": "None",
            "pathological_tum_size": "None"
            }
        }
    }
''')


class MLSuccessResponse(BaseModel):
    __root__: dict = machine_learning
