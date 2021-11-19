from matplotlib_utils import *
import pandas as pd
import os
import numpy as np

indicators_list = [ "GIB01_risk",
                    "GIB01_admission" ]

if not (OUTPUT_DIR / 'figures').exists():
    os.mkdir(OUTPUT_DIR / 'figures')

for i in indicators_list:
    # indicator plots
    df = pd.read_csv(OUTPUT_DIR / f"measure_ce2_indicator_{i}_rate.csv", parse_dates=["date"])
    df = drop_irrelevant_practices(df, "practice_id")

    df["rate"] = df[f"value"]
    df = df.drop(["value"], axis=1)

    # Need this for dummy data
    df = df.replace(np.inf, np.nan) 

    deciles_chart(df,
                  filename=f"plot_{i}",
                  period_column="date",
                  column="rate",
                  count_column = f"indicator_{i}_numerator",
                  ylabel="Proportion",
                  )
