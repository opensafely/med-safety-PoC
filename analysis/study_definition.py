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
)
