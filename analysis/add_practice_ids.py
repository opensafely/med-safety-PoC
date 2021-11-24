from matplotlib_utils import *
from utils import *
import pandas as pd
import os
import numpy as np

for file in DUMMY_DIR.iterdir():
    if match_input_csv_files(file.name):
        print( f"Reading file {file.name}" )
        df = pd.read_csv(DUMMY_DIR / file.name)
        df['practice_id'] = np.random.uniform(low=1, high=50, size=df.shape[0]).astype(int)
        new_file = file.name.replace("input","input_expanded")
        df.to_csv(DUMMY_DIR / f"{new_file}", index=False)
