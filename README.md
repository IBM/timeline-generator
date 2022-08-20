# Timeline-Generator

Create visual timelines for post-incident investigations and other purposes.

## Purpose

Easy creation of pretty, detailed, repeatable, and customizable timelines based on structured data.

I wanted to be able to put all timeline data into a structured format and use that to generate one or more visualizations. 

I played with both [mermaid.js](https://mermaid-js.github.io/mermaid/#/) and [PlantUML](https://plantuml.com/) which are awesome, however neither does a good job of representing detailed timelines.

After using Excel to create a few timelines, I decided to start using matplotlib because it makes a lot more sense to do this in code.

## Features

- Milestones (an event that occurs at a specific time)
- Spans (an event that has a start time and an end time)
- Several customization options
- Use any date/time format understood by [pandas.to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html)
- Save timelines to PNG, SVG, PDF (type detected by output filename)

## Prerequisites

- Python 3
- pandas library (e.g. `pip install pandas`)
- matplotlib library (e.g. `pip install matplotlib`)

## Using

### Create the data files

The first step is to create CSV files for the *milestones* and *spans*.

- Milestones CSV: The Milestone CSV takes the following format: `date,height,description`:
  - `date`: The location of the milestone
  - `height`: The vertical height of the milestone in the visualization
  - `description`: The annotation text that appears next to the milestone
- Spans CSV: The Spans CSV takes the following format: `start,end,height,color,alpha,description`:
  - `start`: The start of the span
  - `end`: The end of the span
  - `height`: The vertical height of the span in the visualization
  - `description`: The annotation text that appears next to the span
  - `color`, `alpha`: self-explanatory 

### Customization Options

- Milestone and Span options are provided as an array of dictionaries. The `index` element of the dictionary determines which milestone or span the options refer to.
- Optional milestone annotation options:
  - `line_width`: Number of characters before wrapping the description.  Default = `300`
  - `x_offset`: Horizontal distance in pixels between the milestone marker and the start of the label. Default = `10`.
  - `y_offset`: Vertical distance in pixels between the milestone marker and the start of the label. Distance in pixels between the milestone marker and the start of the label. Default = `10`. 
  - `arrowprops`: A Dict describing the arrow between the text and the marker.  See [pyplot.annotate](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.annotate.html) for details.
  - `horizontalalignment`: Default is `left`.
- Optional span annotation options:
  - All milestone options above
  - `annotation_point`: Use `end_datetime` to anchor the description at the end of the span.  The default is to anchor at the start of the span.
- Customizing the x-axis: The `interval` parameter determines the distance (in hours) between x-ticks. The default is `24`.

### Running

`timeline-generator` can be used from command line or from a jupyter notebook. Examples of each can be found in the `demo` folder.

Use `sys.path.append` to point to the location of `timeline_generator.py`. You can use a `git submodule` if you want to be fancy.

```
import pandas as pd
import sys
sys.path.append('../') 

from timeline_generator import get_timeline

milestones = pd.read_csv("milestones.csv")
spans = pd.read_csv("spans.csv")

get_timeline(
    milestones,spans,'2022-06-05 12:00','2022-06-14',
    milestone_options=[
        {'index':0,'line_width':30.},
        {'index':1,'line_width':50.}
    ],
    filename='timeline-1.png'
)
```