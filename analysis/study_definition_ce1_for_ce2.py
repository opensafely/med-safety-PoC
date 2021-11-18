from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

from codelists import *

start_date = "2020-01-01"
end_date = "2020-03-01"


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

study = StudyDefinition(
    index_date=start_date,

    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },

    population=patients.all(),

    # registered=patients.registered_as_of("index_date"),

    # died=patients.died_from_any_cause(
    #     on_or_before="index_date",
    #     returning="binary_flag",
    #     return_expectations={"incidence": 0.1}
    # ),

    # practice=patients.registered_practice_as_of(
    #     "index_date",
    #     returning="pseudo_id",
    #     return_expectations={
    #         "int": {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence": 0.5}
    # ),


    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    # _age_65_plus=patients.satisfying(
    #     """
    #     (age >=65)
    #     """,
    # ),

    # sex=patients.sex(
    #     return_expectations={
    #         "rate": "universal",
    #         "category": {"ratios": {"M": 0.5, "F": 0.5}},
    #     }
    # ),

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
        codelist=oral_nsaid_drugs_codelist,
        find_first_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    ppi=patients.with_these_medications(
        codelist=ulcer_healing_drugs_codelist,
        find_first_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
    ),

    indicator_GIB01_risk_denominator=patients.satisfying(
        """
        oral_nsaid AND
        (age >=65)
        """,
    ),

    indicator_GIB01_risk_numerator=patients.satisfying(
        """
        (NOT ppi) AND
        (age >=65) AND
        oral_nsaid
        """,
    ),

    # GIB01 / admission indicator --------------------------------- #
    # Patients 65 years or over admitted to hospital with a
    # gastro-intestinal bleed and currently prescribed an NSAID and
    # NOT concurrently prescribed a gastro-protective medicine.

    # NB all data in OpenSafely are completed spells so we do not
    # need to request episodes that are completed.

    GIB_admission=patients.admitted_to_hospital(
        with_these_primary_diagnoses=GIB_admissions_codelist,
        with_admission_method=emergency_admission_codes,
        find_last_match_in_period=True,
        returning="binary_flag",
        between=["index_date - 3 months", "index_date"],
        return_expectations={
            "incidence": 0.6,
            "int": {"distribution": "normal", "mean": 8, "stddev": 2},
        },
    ),

    indicator_GIB01_admission_numerator = patients.satisfying(
        """
        indicator_GIB01_risk_numerator AND
        ( GIB_admission )
        """
    ),


    indicator_GIB01_admission_denominator = patients.satisfying(
        """
        indicator_GIB01_risk_numerator
        """
    ),

    practice_id=patients.admitted_to_hospital(
        with_these_primary_diagnoses=GIB_admissions_codelist,
        with_admission_method=emergency_admission_codes,
        returning="number_of_matches_in_period",
        between=["index_date - 3 months", "index_date"],
        return_expectations={
            "incidence": 1.0,
            "int": {"distribution": "normal", "mean": 8, "stddev": 3},
        },
    ),


    # # AKI01 ======================================================= #

    # # AKI01 / increased risk indicator ---------------------------- #
    # # Patients prescribed a non-steroidal anti-inflammatory drug
    # # (NSAID), a renin-angiotensin system (RAS) drug and a diuretic
    # # and therefore potentially at increased risk of admission to
    # # hospital with acute kidney injury(AKI)

    # ras=patients.with_these_medications(
    #     codelist=PLACEHOLDER_drugs_codelist,
    #     find_last_match_in_period=True,
    #     returning="binary_flag",
    #     between=["index_date - 3 months", "index_date"],
    # ),

    # diuretic=patients.with_these_medications(
    #     codelist=PLACEHOLDER_drugs_codelist,
    #     find_last_match_in_period=True,
    #     returning="binary_flag",
    #     between=["index_date - 3 months", "index_date"],
    # ),

    # indicator_AKI01_risk_denominator=patients.satisfying(
    #     """
    #     oral_nsaid OR ras OR diuretic
    #     """,
    # ),

    # indicator_AKI01_risk_numerator=patients.satisfying(
    #     """
    #     oral_nsaid AND ras AND diuretic
    #     """,
    # ),

    # # AKI01 / admissions indicator -------------------------------- #
    # # Patients 18 years old or over admitted to hospital with acute
    # # kidney injury prescribed a non-steroidal anti-inflammatory drug
    # # (NSAID), a reninangiotensin system(RAS) drug and a diuretic

    # indicator_AKI01_admission_count=patients.admitted_to_hospital(
    #     with_these_primary_diagnoses=PLACEHOLDER_admissions_codelist,
    #     with_admission_method=emergency_admission_codes,
    #     returning="number_of_matches_in_period",
    #     between=["index_date - 3 months", "index_date"],
    #     return_expectations={
    #         "incidence": 0.6,
    #         "int": {"distribution": "normal", "mean": 8, "stddev": 2},
    #     },
    # ),

    # indicator_AKI01_admission_numerator=patients.satisfying(
    #     """
    #     indicator_AKI01_risk_numerator AND
    #     ( indicator_AKI01_admission_count > 0 )
    #     """
    # ),

    # # PAIN01 ======================================================= #

    # # PAIN01 / increased risk indicator ---------------------------- #
    # # Number of patients concurrently prescribed an oral or
    # # transdermal opioid and a benzodiazepine, Z-drug, pregabalin or
    # # gabapentin and therefore potentially at increased risk of
    # # admission to hospital for respiratory depression, overdose
    # # (accidental) or confusion.

    # opioid=patients.with_these_medications(
    #     codelist=PLACEHOLDER_drugs_codelist,
    #     find_last_match_in_period=True,
    #     returning="binary_flag",
    #     between=["index_date - 3 months", "index_date"],
    # ),

    # sedative=patients.with_these_medications(
    #     codelist=PLACEHOLDER_drugs_codelist,
    #     find_last_match_in_period=True,
    #     returning="binary_flag",
    #     between=["index_date - 3 months", "index_date"],
    # ),

    # indicator_PAIN01_risk_denominator=patients.satisfying(
    #     """
    #     opioid OR sedative
    #     """,
    # ),

    # indicator_PAIN01_risk_numerator=patients.satisfying(
    #     """
    #     opioid AND sedative
    #     """,
    # ),

    # # PAIN01 / admissions indicator -------------------------------- #
    # # Patients 18 years old or over admitted to hospital for
    # # respiratory depression, overdose (accidental) or confusion
    # # concurrently prescribed an oral or transdermal opioid and a
    # # benzodiazepine, Z-drug, pregabalin or gabapentin.

    # indicator_PAIN01_admission_count=patients.admitted_to_hospital(
    #     with_these_primary_diagnoses=PLACEHOLDER_admissions_codelist,
    #     with_admission_method=emergency_admission_codes,
    #     returning="number_of_matches_in_period",
    #     between=["index_date - 3 months", "index_date"],
    #     return_expectations={
    #         "incidence": 0.6,
    #         "int": {"distribution": "normal", "mean": 8, "stddev": 2},
    #     },
    # ),

    # indicator_PAIN01_admission_numerator=patients.satisfying(
    #     """
    #     indicator_PAIN01_risk_numerator AND
    #     ( indicator_PAIN01_admission_count > 0 )
    #     """
    # ),



)
