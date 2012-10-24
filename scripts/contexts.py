from matplotlib import pyplot
import math
from matplotlib.patches import Ellipse
import random
import numpy as np

import ipdb

random.seed(5)

DIM = 21

points = []
for i in range(DIM):
    for j in range(DIM):
        points.append((i, j))

figure = pyplot.figure(figsize=(9, 3))
plots = [figure.add_subplot(1, 3, i + 1) for i in range(3)]

MID = int(DIM/2)
selection = [[(MID, MID)], [(MID, MID)], [(MID, MID)]]
contexts = [[], [], []]
others = [[], [], []]

for pt in points:
    dx = pt[0] - MID 
    dy = pt[1] - MID
    d = math.sqrt(dx * dx + dy * dy)

    if d < 1:
        selection[0].append(pt)
    else:
        contexts[0].append(pt)

    if d < 1:
        selection[1].append(pt)
    elif d < 5:
        contexts[1].append(pt)
    else:
        others[1].append(pt)

    dx = pt[0] - MID + 1 
    dy = pt[1] - MID
    d = min(d, math.sqrt(dx * dx + dy * dy))
    dx = pt[0] - MID - 1 
    dy = pt[1] - MID - 1
    d = min(d, math.sqrt(dx * dx + dy * dy))
    dx = pt[0] - MID - 2 
    dy = pt[1] - MID + 5
    d = min(d, math.sqrt(dx * dx + dy * dy))
    dx = pt[0] - MID + 2 
    dy = pt[1] - MID - 2
    d = min(d, math.sqrt(dx * dx + dy * dy))
    
    if d < 1: 
        selection[2].append(pt)
    elif d < 5:
        contexts[2].append(pt)
    else:
        others[2].append(pt)

for i in range(3):
    plot = plots[i]

    (selectionx, selectiony) = zip(*selection[i])
    plot.scatter(selectionx, selectiony, marker='o', color='k')

    (contextx, contexty) = zip(*contexts[i])
    plot.scatter(contextx, contexty, marker='o', color='0.6')

    if len(others[i]) > 0:
        (otherx, othery) = zip(*others[i])
        plot.scatter(otherx, othery, marker='o', color='0.9')

for plot in plots:
    a = 0.5
    plot.set_xlim([0 - a, DIM - a])
    plot.set_ylim([0 - a, DIM - a])
    plot.set_xticks([])
    plot.set_yticks([])
    #plot.set_axis_off()

figure.tight_layout()

figure.show()

pyplot.savefig('../resources/contextz.eps', bbox_inches='tight')
