from cohortextractor import (
    codelist_from_csv,
)

ulcer_healing_drugs_codelist = codelist_from_csv("codelists/pincer-ppi.csv",
                                 system="snomed",
                                 column="id",)

oral_nsaid_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                 system="snomed",
                                 column="id",)

#####################################################################
### TO UPDATE ONCE CODELISTS HAVE BEEN CREATED ######################
#####################################################################

gi_admissions_codelist = codelist_from_csv("codelists/opensafely-acute-transverse-myelitis-icd-10-323243cb.csv",
                                           system="icd10",
                                           column="code",)

ras_drugs_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                       system="snomed",
                                       column="id",)

### Note - a PINCER "loop diuretics" list already exists - could this
### be used here?
diuretics_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                            system="snomed",
                                            column="id",)
