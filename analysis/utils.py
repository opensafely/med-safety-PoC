import dateutil
import pandas as pd
from pathlib import Path
import numpy as np
import re

BASE_DIR = Path(__file__).parents[1]
DUMMY_DIR = BASE_DIR / "output" / "ce1"
OUTPUT_DIR = BASE_DIR / "output" / "ce2"

NUM_PATIENTS = 5000

def add_months(date_in, delta_months):
    index_date = pd.to_datetime(date_in)
    month_delta = dateutil.relativedelta.relativedelta(months=delta_months)
    new_date = index_date + month_delta
    new_date_string = f"{new_date.year}-{str(new_date.month).zfill(2)}-{str(new_date.day).zfill(2)}"
    return(new_date_string)


def match_input_csv_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_.*_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv"
    return True if re.match(pattern, file) else False
