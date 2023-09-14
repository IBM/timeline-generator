import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import textwrap

def get_timeline(data, start=None, end=None,
                 granularity='hours', interval=24, ylim=None, dateformat='%a %b %d', fig_height=5, fig_width=14, filename=None):

    data['start_datetime'] = pd.to_datetime(data.start, format='mixed')
    data['end_datetime'] = pd.to_datetime(data.end, format='mixed')

    offset_args = {}
    offset_args[granularity] = interval
    if not start:
        start_datetime = min(data.start_datetime) - \
            pd.DateOffset(**offset_args)
    else:
        start_datetime = pd.to_datetime(start)
    if not end:
        end_datetime = max(max(data.start_datetime), max(
            data.end_datetime)) + pd.DateOffset(**offset_args)
    else:
        end_datetime = pd.to_datetime(end)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=300)
    ax.set_xlim([start_datetime, end_datetime])
    if not ylim:
        ax.set_ylim(0,1+data[
            ((data.start_datetime >= start_datetime) & (data.start_datetime <= end_datetime)) | 
            (pd.notnull(data.end_datetime) & (data.end_datetime >= start_datetime) & (data.end_datetime <= end_datetime))
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
    for index, row in plots.iterrows():
        ax.plot(row.start_datetime, row.height, row.markerfmt,
                color=row.color, markerfacecolor=row.color)
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
    if granularity == 'minutes':
        ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=interval))
    elif granularity == 'hours':
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
    elif granularity == 'weeks':
        ax.xaxis.set_major_locator(mdates.WeekLocator(interval=interval)) 
    elif granularity == 'months':
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval)) 
    else:
        print("invalid granularity")
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
        'textcolor': 'black',
        'alpha': 1,
        'linewidth': 20,
        'vline': True,
        'marker': True,
        'markerfmt': 'o',
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
    if pd.isna(row['arrowprops']):
        row['arrowprops'] = None
    ax.annotate(
        description, xy=(anchor, row.height),
        xytext=(row.x_offset, row.y_offset), 
        textcoords="offset points",
        horizontalalignment=row.horizontalalignment,
        verticalalignment="top",
        color=row.textcolor,
        arrowprops=row.arrowprops
    )
