from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

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
)
