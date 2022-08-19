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