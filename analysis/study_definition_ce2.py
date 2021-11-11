from cohortextractor import categorise, codelist, table

from codelists import *

start_date = "2019-09-01"
end_date = "2021-07-01"
index_date = start_date

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

# Example study definitions for v2
# https: // github.com/opensafely/SRO-Measures/blob/rebkwok/v2/analysis/study_definition.py
# https: // github.com/opensafely/long-covid/blob/simplified-for-ce2/analysis/study_definition_cohort_v2.py


class Cohort:

    # Population ================================================== #
    _registrations = table("practice_registrations").date_in_range(index_date)
    # There can be more than one registration per patient, get the latest one
    _latest_registrations = _registrations.latest("date_end")
    practice = _latest_registrations.get("pseudo_id")
    population = _registrations.exists()

    ### TO REVISIT: identify which patients are still alive

    # Demographics ================================================ #
    # Age --------------------------------------------------------- #
    _age = table("patients").age_as_of(index_date)
    _age_categories = {
        "0-17": _age < 18,
        "18-24": (_age >= 18) & (_age < 25),
        "25-34": (_age >= 25) & (_age < 35),
        "35-44": (_age >= 35) & (_age < 45),
        "45-54": (_age >= 45) & (_age < 55),
        "55-69": (_age >= 55) & (_age < 70),
        "70-79": (_age >= 70) & (_age < 80),
        "80+": _age >= 80,
    }
    age_group = categorise(_age_categories, default="missing")

    # Sex
    ### TO REVISIT: sex = table("patients").get("sex")

    # Region
    region = _latest_registrations.get("nuts1_region_name")

    # IMD
    _imd_value = table("patient_address").imd_rounded_as_of(index_date)
    _imd_groups = {
        "1": (_imd_value >= 1) & (_imd_value < (32844 * 1 / 5)),
        "2": (_imd_value >= 32844 * 1 / 5) & (_imd_value < (32844 * 2 / 5)),
        "3": (_imd_value >= 32844 * 2 / 5) & (_imd_value < (32844 * 3 / 5)),
        "4": (_imd_value >= 32844 * 3 / 5) & (_imd_value < (32844 * 4 / 5)),
        "5": (_imd_value >= 32844 * 4 / 5) & (_imd_value < 32844),
    }
    imd = categorise(_imd_groups, default="0")

    # Ethnicity
    ethnicity = (
        table("clinical_events")
        .filter("code", is_in=ethnicity_codes)
        .filter("date", on_or_before=index_date)
        .latest()
        .get("code")
    )
