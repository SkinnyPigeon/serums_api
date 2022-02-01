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
