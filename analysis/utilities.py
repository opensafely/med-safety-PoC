import dateutil
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output" / "ce2"

def add_months(date_in, delta_months):
    index_date = pd.to_datetime(date_in)
    month_delta = dateutil.relativedelta.relativedelta(months=delta_months)
    new_date = index_date + month_delta
    new_date_string = f"{new_date.year}-{str(new_date.month).zfill(2)}-{str(new_date.day).zfill(2)}"
    return(new_date_string)

#####################################################################
### Functions related to decile chart creation ######################
#####################################################################

BEST = 0
UPPER_RIGHT = 1
UPPER_LEFT = 2
LOWER_LEFT = 3
LOWER_RIGHT = 4
RIGHT = 5
CENTER_LEFT = 6
CENTER_RIGHT = 7
LOWER_CENTER = 8
UPPER_CENTER = 9
CENTER = 10

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


def deciles_chart(df, filename, period_column=None, column=None, count_column=None, title="", ylabel="", time_window=""):
    """period_column must be dates / datetimes"""

    df = compute_redact_deciles(df, period_column, count_column, column)
    
    """period_column must be dates / datetimes"""
    sns.set_style("whitegrid", {"grid.color": ".9"})
    
    fig, ax = plt.subplots(1, 1)
    
    linestyles = {
        "decile": {
            "line": "b--",
            "linewidth": 1,
            "label": "Decile",
        },
        "median": {
            "line": "b-",
            "linewidth": 1.5,
            "label": "Median",
        },
        "percentile": {
            "line": "b:",
            "linewidth": 0.8,
            "label": "1st-9th, 91st-99th percentile",
        },
    }
    label_seen = []
    for percentile in range(1, 100):  # plot each decile line
        data = df[df["percentile"] == percentile]
        add_label = False

        if percentile == 50:
            style = linestyles["median"]
            add_label = True
        
        else:
            style = linestyles["decile"]
            if "decile" not in label_seen:
                label_seen.append("decile")
                add_label = True
        if add_label:
            label = style["label"]
        else:
            label = "_nolegend_"

        ax.plot(
            data[period_column],
            data[column],
            style["line"],
            linewidth=style["linewidth"],
            label=label,
        )
    ax.set_ylabel(ylabel, size=15, alpha=0.6)
    if title:
        ax.set_title(title, size=14, wrap=True)
    # set ymax across all subplots as largest value across dataset
    
    ax.set_ylim([0, 1 if df[column].isnull().values.all() else df[column].max() * 1.05])
    ax.tick_params(labelsize=12)
    ax.set_xlim(
        [df[period_column].min(), df[period_column].max()]
    )  # set x axis range as full date range

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%B %Y"))
  
    
    plt.xticks(sorted(df[period_column].unique()),rotation=90)
    
    plt.vlines(x=[pd.to_datetime("2020-03-01")], ymin=0, ymax=1, colors='orange', ls='--', label='National Lockdown')
    
    if not time_window=="":

        plt.vlines(x=[pd.to_datetime(time_window)],ymin=0, ymax=1, colors='green', ls='--', label='Date of expected impact')
    
    ax.legend(
        bbox_to_anchor=(1.1, 0.8),  # arbitrary location in axes
        #  specified as (x0, y0, w, h)
        loc=CENTER_LEFT,  # which part of the bounding box should
        #  be placed at bbox_to_anchor
        ncol=1,  # number of columns in the legend
        fontsize=8,
        borderaxespad=0.0,
    )  # padding between the axes and legend
        #  specified in font-size units
  
    
    plt.tight_layout()
    plt.savefig(f"output/ce2/figures/{filename}.jpeg")
    plt.clf()


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
