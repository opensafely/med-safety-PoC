from cohortextractor import table, codelist #, categorise
from codelists import *

# Example study definitions for v2
# https: // github.com/opensafely/SRO-Measures/blob/v2/analysis/study_definition.py
# --> graphnet backend example
# https: // github.com/opensafely/long-covid/blob/simplified-for-ce2/analysis/study_definition_cohort_v2.py
# --> TPP backend example

# https://github.com/opensafely-core/cohort-extractor-v2/blob/18a92af5fbf5ccc31725279cb087788fa2c98209/tests/backends/test_databricks.py#L87-L94
# --> testing for databricks backend (includes prescription query)

# https://github.com/opensafely-core/cohort-extractor-v2/blob/main/cohortextractor/backends/databricks.py
# table( "patients"      ) - date_of_birth (date)
# table( "prescriptions" ) - patient_id (integer)
#                          - prescribed_dmd_code (dmd)
#                          - processing_date (date)
# table( "hospital_admissions ) - admission_date (date)
#                               - primary_diagnosis (icd10)
#                               - admission_method (integer)
#                               - episode_is_finished (boolean)
#                               - spell_id (integer)

emergency_admission_codes = [
    "21",  # Emergency Admission: Emergency Care Department or dental casualty department of the Health Care Provider
    "22",  # Emergency Admission: GENERAL PRACTITIONER: after a request for immediate admission has been made direct to a Hospital Provider, i.e. not through a Bed bureau, by a GENERAL PRACTITIONER or deputy
    "23",  # Emergency Admission: Bed bureau
    "24",  # Emergency Admission: Consultant Clinic, of this or another Health Care Provider
    "25",  # Emergency Admission: Admission via Mental Health Crisis Resolution Team
    "2A",  # Emergency Admission: Emergency Care Department of another provider where the PATIENT  had not been admitted
    "2B",  # Emergency Admission: Transfer of an admitted PATIENT from another Hospital Provider in an emergency
    "2D",  # Emergency Admission: Other emergency admission
    "28"   # Emergency Admission: Other means, examples are:
           # - admitted from the Emergency Care Department of another provider where they had not been admitted
           # - transfer of an admitted PATIENT from another Hospital Provider in an emergency
           # - baby born at home as intended
]

emergency_admission_codes_integers = [21, 22, 23, 24, 25, 28]


class Cohort:
    population = table("patients").exists()
    dob = table("patients").first_by("patient_id").get("date_of_birth")
    age = table("patients").age_as_of("2020-01-01")

    oral_nsaid = (
        table("prescriptions")
        .filter("processing_date", between=["2020-01-01", "2020-01-31"])
        .filter("prescribed_dmd_code", is_in=oral_nsaid_drugs_codelist )
        .exists()
    )

    GIB_admission = (
        table("hospital_admissions")
        .filter("admission_date", between=["2020-01-01", "2020-01-31"])
        .filter("primary_diagnosis", is_in=PLACEHOLDER_admissions_codelist )
        .filter(episode_is_finished=True)
        .filter("admission_method", is_in=emergency_admission_codes_integers)
        .exists()
    )
