import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import textwrap

def get_timeline(data, start=None, end=None,
                 interval=24, ylim=None, dateformat='%a %b %d', filename=None):

    data['start_datetime'] = pd.to_datetime(data.start)
    data['end_datetime'] = pd.to_datetime(data.end)

    if not start:
        start_datetime = min(data.start_datetime) - \
            pd.DateOffset(hours=interval)
    else:
        start_datetime = pd.to_datetime(start)
    if not end:
        end_datetime = max(max(data.start_datetime), max(
            data.end_datetime)) + pd.DateOffset(hours=interval)
    else:
        end_datetime = pd.to_datetime(end)

    fig, ax = plt.subplots(figsize=(14, 5), dpi=300)
    ax.set_xlim([start_datetime, end_datetime])
    if not ylim:
        ax.set_ylim(0,1+data[
            (data.start_datetime > start_datetime) & (data.start_datetime < end_datetime)
            ].height.max())
    else:
        ax.set_ylim(0,ylim)

    data['options'] = data.apply(lambda row: set_defaults(row.options), axis=1)
    data_options = pd.DataFrame([x for x in data.options])
    data = data.combine_first(data_options)
    data = data.where(pd.notnull(data), None)

    spans = data[data.end_datetime.notnull()]
    if spans.shape[0] > 0:
        ax.hlines(spans.height, spans.start_datetime, spans.end_datetime,
                  linewidth=spans.linewidth, capstyle='round', alpha=spans.alpha,
                  color=spans.color)
    milestones = data[data.end_datetime.isnull()]
    vlines = milestones[milestones.vline == True]
    plots = milestones[milestones.marker == True]
    ax.plot(plots.start_datetime, plots.height, "o",
            color='darkblue', markerfacecolor="darkblue")
    ax.vlines(vlines.start_datetime, 0, vlines.height,
              color=vlines.color, linewidth=0.5)
    data.apply(lambda row: annotate(ax, row), axis=1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.get_yaxis().set_ticks([])
    dtFmt = mdates.DateFormatter(dateformat)  # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
    ax.tick_params(axis="x", labelsize=8)
    fig.autofmt_xdate()
    if (filename):
        plt.savefig(filename, bbox_inches='tight')
    return ax

def set_defaults(options):
    defaults = {
        'text_wrap': 50,
        'x_offset': 10,
        'y_offset': 5,
        'arrowprops': None,
        'annotation_anchor': 'left',
        'horizontalalignment': 'left',
        'color': 'darkblue',
        'alpha': 1,
        'linewidth': 20,
        'vline': True,
        'marker': True,
        'placement':'right'
    }
    result = defaults
    for option in options:
        result[option] = options[option]
    return result


def annotate(ax, row):
    description = "\n".join(textwrap.wrap(
        row.description, width=row['text_wrap']))
    if row['annotation_anchor'] == 'left':
        anchor = row['start_datetime']
    elif row['annotation_anchor'] == 'right':
        anchor = row['end_datetime']
    elif row['annotation_anchor'] == 'start':
        anchor = mdates.num2date(ax.get_xlim()[0])
    elif row['annotation_anchor'] == 'end':
        anchor = mdates.num2date(ax.get_xlim()[1])
    if row['placement'] == 'left':
        row['horizontalalignment'] = 'right'
        row['x_offset'] = -10
    ax.annotate(description, xy=(anchor, row.height),
                xytext=(row.x_offset, row.y_offset
                        ), textcoords="offset points",
                horizontalalignment=row.horizontalalignment,
                verticalalignment="top",
                arrowprops=row.arrowprops)
