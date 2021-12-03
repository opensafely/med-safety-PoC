from comp_deciles import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

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
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%B %Y"))
  
    
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
