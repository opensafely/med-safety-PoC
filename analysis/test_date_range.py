from cohortextractor import cohort_date_range, table


index_date_range = cohort_date_range(
    start="2021-01-01", end="2021-03-01", increment="month"
)

def cohort(index_date):
    class Cohort:
        population = table("patients").exists()
        dob = table("patients").first_by("patient_id").get("date_of_birth")
        age = table("patients").age_as_of(index_date)

    return Cohort
