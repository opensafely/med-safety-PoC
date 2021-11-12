from cohortextractor import table, codelist #, categorise
# from codelists import *

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



class Cohort:
    population = table("patients").exists()
    # dob = table("patients").first_by("patient_id").get("date_of_birth")
    # age = table("patients").age_as_of("2020-01-01")

    # prescribed_med = (
    #     table("prescriptions")
    #     .filter("processing_date", between=["2020-01-01", "2020-01-31"])
    #     .filter(
    #         "prescribed_dmd_code", is_in=codelist(["0010", "0050"], system="dmd")
    #     )
    #     .exists()
    # )

    # admitted = (
    #     table("hospital_admissions")
    #     .filter("admission_date", between=["2020-01-01", "2020-01-31"])
    #     .filter(primary_diagnosis="N05", episode_is_finished=True)
    #     .filter("admission_method", between=[20, 29])
    #     .exists()
    # )
