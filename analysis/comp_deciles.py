import pandas as pd
from pathlib import Path
import numpy as np

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output" / "ce2"

#####################################################################
### Functions related to decile chart calculations ##################
#####################################################################

def compute_deciles(
    measure_table, groupby_col, values_col, has_outer_percentiles=True
):
    """Computes deciles.
    Args:
        measure_table: A measure table.
        groupby_col: The name of the column to group by.
        values_col: The name of the column for which deciles are computed.
        has_outer_percentiles: Whether to compute the nine largest and nine smallest
            percentiles as well as the deciles.
    Returns:
        A data frame with `groupby_col`, `values_col`, and `percentile` columns.
    """
    quantiles = np.arange(0.1, 1, 0.1)
    if has_outer_percentiles:
        quantiles = np.concatenate(
            [quantiles, np.arange(0.01, 0.1, 0.01), np.arange(0.91, 1, 0.01)]
        )

    percentiles = (
        measure_table.groupby(groupby_col)[values_col]
        .quantile(pd.Series(quantiles, name="percentile"))
        .reset_index()
    )
    percentiles["percentile"] = percentiles["percentile"].apply(
        lambda x: int(x * 100))

    return percentiles

def compute_redact_deciles(df, period_column, count_column, column):
    n_practices = df.groupby(by=['date'])[['practice_id']].nunique()

    count_df = compute_deciles(measure_table=df, groupby_col=period_column,
                               values_col=count_column, has_outer_percentiles=False)
    quintile_10 = count_df[count_df['percentile']
                           == 10][['date', count_column]]
    df = compute_deciles(df, period_column, column, False).merge(
        n_practices, on="date").merge(quintile_10, on="date")

    # if quintile 10 is 0, make sure at least 5 practices have 0. If >0, make sure more than 5 practices are in this bottom decile
    df['drop'] = (
        (((df['practice_id']*0.1) * df[count_column]) <= 5) & (df[count_column] != 0) |
        ((df[count_column] == 0) & (df['practice_id'] <= 5))
    )

    df.loc[df['drop'] == True, ['rate']] = np.nan

    return df

def drop_irrelevant_practices(df,practice_column):
    """Drops irrelevant practices from the given measure table.
    An irrelevant practice has zero events during the study period.
    Args:
        df: A measure table.
    Returns:
        A copy of the given measure table with irrelevant practices dropped.
    """
    is_relevant = df.groupby(practice_column).value.any()
    return df[df[practice_column].isin(is_relevant[is_relevant == True].index)]
