import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import textwrap

def get_timeline(milestones, spans, start, end, 
                 milestone_options=[], span_options=[], interval=24, filename=None):

    start_datetime = pd.to_datetime(start)
    end_datetime = pd.to_datetime(end)

    fig, ax = plt.subplots(figsize=(14, 5), dpi=300)

    # create the milestones (vertical lines and markers)
    ax.vlines(milestones.datetime, 0, milestones.height,
              color="darkblue", linewidth=0.5)
    ax.plot(milestones.datetime, milestones.height, "o",
            color="darkblue", markerfacecolor="w")  
    annotate(ax, milestones, milestone_options)

    # create the spans (horizontal bars)
    spans['start_datetime'] = pd.to_datetime(spans.start)
    spans['end_datetime'] = pd.to_datetime(spans.end)

    ax.hlines(spans.height, spans.start_datetime, spans.end_datetime,
              linewidth=20, capstyle='round', alpha=spans.alpha, color=spans.color)
    annotate(ax, spans, span_options)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.set_xlim([start_datetime, end_datetime])
    ax.get_yaxis().set_ticks([])
    dtFmt = mdates.DateFormatter('%a %b %d')  # define the formatting
    ax.xaxis.set_major_formatter(dtFmt)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
    ax.tick_params(axis="x", labelsize=8)
    fig.autofmt_xdate()
    if (filename):
        plt.savefig(filename, bbox_inches='tight')

def annotate(ax, data, data_options):
    if 'start_datetime' not in data.columns:
        data['start_datetime'] = pd.to_datetime(data.date)

    for i in data.index:
        data_hash = {}
        for option in data_options:
            data_hash[option['index']] = option
        override_options = data_hash.get(i, {})
        options = {
            'line_width': 300.,
            'x_offset': 10,
            'y_offset': 0,
            'arrowprops': None,
            'annotation_point': 'start_datetime',
            'horizontalalignment': 'left'
        }
        for option in override_options:
            options[option] = override_options[option]
        d = data.loc[i, options['annotation_point']]
        height = data.loc[i, 'height']
        description = "\n".join(textwrap.wrap(
            data.loc[i, 'description'], width=options['line_width']))
        ax.annotate(description, xy=(d, height),
                    xytext=( options['x_offset'], options['y_offset']), textcoords="offset points",
            horizontalalignment=options['horizontalalignment'],
            verticalalignment="center",
            arrowprops=options['arrowprops'])