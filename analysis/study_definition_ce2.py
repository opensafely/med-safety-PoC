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


class Cohort:

    # Population ================================================== #
    _registrations = table("practice_registrations").date_in_range(index_date)
    # There can be more than one registration per patient, get the latest one
    _latest_registrations = _registrations.latest("date_end")
    practice = _latest_registrations.get("pseudo_id")

    # https: // github.com/opensafely/SRO-Measures/blob/rebkwok/v2/analysis/study_definition.py
    _died = table("deaths").filter("date_of_death",
                                   on_or_before=index_date).exists()
    population = _registrations.exists() & ~(_died.exists())
