import dateutil
import pandas as pd

def add_months(date_in, delta_months):
    index_date = pd.to_datetime(date_in)
    month_delta = dateutil.relativedelta.relativedelta(months=delta_months)
    new_date = index_date + month_delta
    new_date_string = f"{new_date.year}-{str(new_date.month).zfill(2)}-{str(new_date.day).zfill(2)}"
    return(new_date_string)