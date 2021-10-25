from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

start_date = "2019-09-01"
end_date = "2021-07-01"

study = StudyDefinition(
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),
)
