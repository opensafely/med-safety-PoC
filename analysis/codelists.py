from databuilder import (
    codelist_from_csv,
    codelist
)

ulcer_healing_drugs_codelist = codelist_from_csv(
    "codelists/pincer-ppi.csv",
    system="snomed",
    column="id",)

oral_nsaid_drugs_codelist = codelist_from_csv(
    "codelists/pincer-nsaid.csv",
    system="snomed",
    column="id",)

gib_admissions_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-gastro-intestinal-bleed.csv",
    system="icd10",
    column="code",)

aki_admissions_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-acute-kidney-injury.csv",
    system="icd10",
    column="code",)

pain_01and03_admissions_diagnosis_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-pain01-pain03-diagnosis.csv",
    system="icd10",
    column="code",)

pain_01and03_admissions_cause_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-pain01-pain03-cause.csv",
    system="icd10",
    column="code",)

pain_02_admissions_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-pain02.csv",
    system="icd10",
    column="code",)

frac_admissions_diagn_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-frac-diagnosis.csv",
    system="icd10",
    column="code",)

frac_acb_admissions_cause_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-frac-acb-cause.csv",
    system="icd10",
    column="code",)

resp_admissions_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-respiratory.csv",
    system="icd10",
    column="code",)

acb_admissions_01_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-anticholinergic-burden-diagnosis-01.csv",
    system="icd10",
    column="code",)

acb_admissions_02_codelist = codelist_from_csv(
    "codelists/nhsbsa-adm-anticholinergic-burden-diagnosis-02.csv",
    system="icd10",
    column="code",)

#####################################################################
### PLACEHOLDER CODELISTS ###########################################
#####################################################################

### ADMISSIONS -------------------------------------------------- ###
PLACEHOLDER_admissions_codelist = codelist(
    [ "K226", "K226", "K226", "K252", "K254", "K256", "K260", "K262", "K264", "K266" ],
    system="icd10")

### DRUGS ------------------------------------------------------- ###
PLACEHOLDER_drugs_codelist = codelist_from_csv("codelists/pincer-nsaid.csv",
                                       system="snomed",
                                       column="id",)

