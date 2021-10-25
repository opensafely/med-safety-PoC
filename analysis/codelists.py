from cohortextractor import (
    codelist_from_csv,
)

ulcer_healing_drugs_codelist = codelist_from_csv("codelists/pincer-ppi.csv",
                                 system="snomed",
                                 column="id",)

oral_nsaid_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                 system="snomed",
                                 column="id",)