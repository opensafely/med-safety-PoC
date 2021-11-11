from cohortextractor import (
    codelist_from_csv,
    codelist
)

ulcer_healing_drugs_codelist = codelist_from_csv("codelists/pincer-ppi.csv",
                                 system="snomed",
                                 column="id",)

oral_nsaid_drugs_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                 system="snomed",
                                 column="id",)

ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity.csv",
    system="ctv3",
    column="Code",
)

#####################################################################
### PLACEHOLDER CODELISTS ###########################################
#####################################################################

### ADMISSIONS -------------------------------------------------- ###
PLACEHOLDER_admissions_codelist = covid_codelist = codelist(
    [ "K226", "K226", "K226", "K252", "K254", "K256", "K260", "K262", "K264", "K266" ],
    system="icd10")

### DRUGS ------------------------------------------------------- ###
PLACEHOLDER_drugs_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                       system="snomed",
                                       column="id",)

