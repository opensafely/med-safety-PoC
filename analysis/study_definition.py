from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from codelists import *

start_date = "2019-09-01"
end_date = "2021-07-01"

study = StudyDefinition(
    index_date=start_date,

    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },

    population=patients.satisfying(
        """
       registered AND
       NOT died
       """
    ),

    registered=patients.registered_as_of("index_date"),

    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1}
    ),

    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    ),

    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),

    #################################################################
    #################################################################
    ### INDICATORS (August 2019 )                                 ###
    #################################################################
    #################################################################


    #################################################################
    ### GI BLEED INDICATORS                                       ###
    #################################################################

    # GIB01 ======================================================= #

    # GIB01 / increased risk indicator ---------------------------- #
    # Patients aged 65 or over currently prescribed a non-steroidal
    # anti-inflammatory drug (NSAID) without a gastro protective
    # medicine and therefore potentially at increased risk of
    # admission to hospital with a GI bleed.

    oral_nsaid=patients.with_these_medications(
        codelist=oral_nsaid_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    ppi=patients.with_these_medications(
        codelist=ulcer_healing_drugs_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    indicator_GIB01_risk_denominator=patients.satisfying(
        """
        (NOT ppi) AND
        (age >=65 AND age <=120)
        """,
    ),

    indicator_GIB01_risk_numerator=patients.satisfying(
        """
        (NOT ppi) AND
        (age >=65 AND age <=120) AND
        oral_nsaid
        """,
    ),

    # GIB01 / admission indicator --------------------------------- #
    # Patients 65 years or over admitted to hospital with a
    # gastro-intestinal bleed and currently prescribed an NSAID and
    # NOT concurrently prescribed a gastro-protective medicine.

    gi_admission_discharged_date=patients.admitted_to_hospital(
        with_these_diagnoses=gi_admissions_codelist,
        with_admission_method=["21",  # Emergency Admission: Emergency Care Department or dental casualty department of the Health Care Provider
                               "22",  # Emergency Admission: GENERAL PRACTITIONER: after a request for immediate admission has been made direct to a Hospital Provider, i.e. not through a Bed bureau, by a GENERAL PRACTITIONER or deputy
                               "23",  # Emergency Admission: Bed bureau
                               "24",  # Emergency Admission: Consultant Clinic, of this or another Health Care Provider
                               "25",  # Emergency Admission: Admission via Mental Health Crisis Resolution Team
                               "2A",  # Emergency Admission: Emergency Care Department of another provider where the PATIENT  had not been admitted
                               "2B",  # Emergency Admission: Transfer of an admitted PATIENT from another Hospital Provider in an emergency
                               "2D",  # Emergency Admission: Other emergency admission
                               "28"],
        returning="date_discharged",
        between=["index_date - 3 months", "index_date"],
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={
            "date": {"earliest": start_date, "latest": end_date},
            "incidence": 0.05,
        },
    ),

    indicator_GIB01_admission_numerator = patients.satisfying(
        """
        (NOT ppi) AND
        (age >=65 AND age <=120) AND
        oral_nsaid AND
        gi_admission_discharged_date
        """
    ),

    indicator_GIB01_admission_denominator=patients.satisfying(
        """
        (NOT ppi) AND
        (age >=65 AND age <=120) AND
        oral_nsaid
        """,
    ),

    # AKI01 ======================================================= #

    # AKI01 / increased risk indicator ---------------------------- #
    # Patients prescribed a non-steroidal anti-inflammatory drug
    # (NSAID), a renin-angiotensin system (RAS) drug and a diuretic
    # and therefore potentially at increased risk of admission to
    # hospital with acute kidney injury(AKI)

    ras=patients.with_these_medications(
        codelist=ras_drugs_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    diuretic=patients.with_these_medications(
        codelist=diuretics_codelist,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    indicator_AKI01_risk_denominator=patients.satisfying(
        """
        oral_nsaid OR ras OR diuretic
        """,
    ),

    indicator_AKI01_risk_numerator=patients.satisfying(
        """
        oral_nsaid AND ras AND diuretic
        """,
    ),


)
