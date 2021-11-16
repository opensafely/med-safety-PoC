from cohortextractor import table, cohort_date_range, Measure, codelist #, categorise
from codelists import *
from utilities import add_months
import re
import pandas as pd

# Example study definitions for v2
# https://github.com/opensafely/SRO-Measures/blob/v2/analysis/study_definition.py
# --> graphnet backend example
# https://github.com/opensafely/long-covid/blob/simplified-for-ce2/analysis/study_definition_cohort_v2.py
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

emergency_admission_codes = (
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
)


index_date_range = cohort_date_range(
    start="2020-01-01", end="2020-03-01", increment="month"
)

def cohort(index_date):
    three_months_previous = add_months( index_date, -3 )

    class Cohort:
        population = table("patients").exists()
        # dob = table("patients").first_by("patient_id").get("date_of_birth")
        age = table("patients").age_as_of(index_date)

        #################################################################
        ### GI BLEED INDICATORS                                       ###
        #################################################################

        # GIB01 ======================================================= #

        # GIB01 / increased risk indicator ---------------------------- #
        # Patients aged 65 or over currently prescribed a non-steroidal
        # anti-inflammatory drug (NSAID) without a gastro protective
        # medicine and therefore potentially at increased risk of
        # admission to hospital with a GI bleed.

        _age_65_plus = age >= 65

        oral_nsaid = (
            table("prescriptions")
            .filter("processing_date", between=[three_months_previous, index_date])
            .filter("prescribed_dmd_code", is_in=oral_nsaid_drugs_codelist )
            .exists()
        )

        ppi = (
            table("prescriptions")
            .filter("processing_date", between=[three_months_previous, index_date])
            .filter("prescribed_dmd_code", is_in=PLACEHOLDER_drugs_codelist)
            .exists()
        )

        indicator_GIB01_risk_denominator = _age_65_plus and oral_nsaid
        indicator_GIB01_risk_numerator = _age_65_plus and oral_nsaid and ppi

        # GIB01 / admission indicator --------------------------------- #
        # Patients 65 years or over admitted to hospital with a
        # gastro-intestinal bleed and currently prescribed an NSAID and
        # NOT concurrently prescribed a gastro-protective medicine.

        # NB all data in OpenSafely are completed spells so we do not
        # need to request episodes that are completed.

        GIB_admission = (
            table("hospital_admissions")
            .filter("admission_date", between=[three_months_previous, index_date])
            .filter("primary_diagnosis", is_in=PLACEHOLDER_admissions_codelist )
            .filter(episode_is_finished=True)
            .filter("admission_method", is_in=emergency_admission_codes)
            .exists()
        )
        
        indicator_GIB01_admission_numerator = GIB_admission and indicator_GIB01_risk_numerator
        indicator_GIB01_admission_denominator = indicator_GIB01_risk_numerator

        measures = []

    ### Identifying all indicators ================================ #

    ### This will identify all attributes of the class Cohort that
    ### match the indicator_regex defined below, and save this to
    ### indicator_variables
    indicator_regex = re.compile("^indicator_.*")
    indicator_variables = list( filter(indicator_regex.match, Cohort.__dict__.keys() ))

    ### This will take these indicator variables and make a dataframe
    ### which will identify numerator/denominator variables pairs
    ### for each indicator; could incorporate a check here to only
    ### look at those indicators that have a numerator AND denominator
    ### defined above.
    indicator_df = pd.DataFrame( data={'v': indicator_variables} )
    indicator_df['name'] = indicator_df['v'].map(lambda x: re.sub("_(numerator|denominator)", "", x ))
    indicator_df['type'] = indicator_df.apply(lambda x: x['v'].replace(f"{x['name']}_", ''), axis=1)

    print( f"Month {index_date}: creating indicator '{set(indicator_df.name)}'" )

    ### This loops through all indicators identified in the process above
    ### and creates the measure from the numerator and denominator
    ### which is (currently) grouped by practice.
    for this_indicator in set(indicator_df.name):
        this_numerator = ( indicator_df
                            .query( f"name == '{this_indicator}'" )
                            .query( f"type == 'numerator'") ).v.str
        this_denominator = ( indicator_df
                            .query( f"name == '{this_indicator}'" )
                            .query( f"type == 'denominator'") ).v.str
        this_rate = f"{this_indicator}_rate"

        Cohort.measures.extend( [
            Measure(
                id=this_rate,
                numerator=this_numerator,
                denominator=this_denominator,
                group_by=["practice"],
            ),
        ]
    )

    return Cohort
