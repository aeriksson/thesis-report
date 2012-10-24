from matplotlib import pyplot
import math
from matplotlib.patches import Ellipse

figure = pyplot.figure(figsize=(8, 8))
plot = figure.gca()

r = 0.8

p0 = [0, r * math.sqrt(3)]
p1 = [r, 0]
p2 = [-r, 0]

ell1xy = [(p0[0] + p1[0])/2.0, (p0[1] + p1[1])/2.0]
ell2xy = [(p0[0] + p2[0])/2.0, (p0[1] + p2[1])/2.0]
ellw = r * 1.5
ellh = r * 2.8
angle = 33

tinyr = r * 0.90
bigr = r * 3.2

tinyc = [p0[0], p0[1] * 0.947]
bigc = [p0[0], p0[1] * .31]

text_settings = {
    'horizontalalignment': 'center',
    'verticalalignment': 'center',
}

plot.text(p0[0], p0[1] * 0.95, 'Evaluation\ndata', **text_settings)
plot.text(p1[0], p1[1] + 0.05, 'Normal\nreference\ndata', **text_settings)
plot.text(p2[0], p2[1] + 0.05, 'Anomalous\nreference\ndata', **text_settings)

e1 = Ellipse(xy=tinyc, width=tinyr, height=tinyr, facecolor='none', ls='solid')
e2 = Ellipse(xy=ell1xy, width=ellw, height=ellh, angle=angle, facecolor='none', ls='dashed')
e3 = Ellipse(xy=ell2xy, width=ellw, height=ellh, angle=-angle, facecolor='none', ls='dashdot')
e4 = Ellipse(xy=bigc, width=bigr, height=bigr, facecolor='none', ls='dotted')
plot.add_artist(e1)
plot.add_artist(e2)
plot.add_artist(e3)
plot.add_artist(e4)

l = 1.3
plot.set_xlim([bigc[0] - l, bigc[0] + l])
plot.set_ylim([bigc[1] - l, bigc[1] + l])

plot.set_xticks([])
plot.set_yticks([])
plot.set_axis_off()

plot.legend((e1, e2, e3, e4), ('Supervised', 'Semi-supervised, normal reference data', 'Semi-supervised, anomalous reference data', 'Unsupervised'), loc='lower center')

figure.tight_layout()

figure.show()

pyplot.savefig('../resources/supervision.eps', bbox_inches='tight')
