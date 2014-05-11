from matplotlib import pyplot
from matplotlib.patches import Circle
import random

random.seed(5)

DIM = 40

points = []
for i in range(DIM):
    for j in range(DIM):
        points.append((i, j))

figure = pyplot.figure(figsize=(12, 3))
plots = [figure.add_subplot(2, 1, i + 1) for i in range(2)]

radius = 0.2

plot = plots[0]

for x in range(DIM):
    p = Circle((x, 0), radius, fc="k")
    plot.add_patch(p)
    plot.annotate('$s_{%s}$' % (x + 1), (x, -0.8), ha='center', size=15)

for (x, i) in zip(range(0, DIM, 4), range(1, DIM, 2)):
    plot.annotate("$e_{%s}$" % i, (x + 1.5, -1.0),
                  (x + 1.5, -2.1),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,widthB=2.7',
                                  fc="w", ec="k"))

for (x, i) in zip(range(2, DIM - 2, 4), range(2, DIM, 2)):
    plot.annotate("$e_{%s}$" % i, (x + 1.5, 0.4),
                  (x + 1.5, 1.4),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,widthB=2.7',
                                  fc="w", ec="k"))

plot = plots[1]

for x in range(DIM):
    if x < 22 and x > 17:
        c = '.0'
    elif x > 5 and x < 34:
        # c = '0.6'
        c = (255 / 255.0, 150 / 255.0, 150 / 255.0)
    else:
        c = '0.9'
    p = Circle((x, 0), radius, color=c)
    plot.add_patch(p)

    if x > 5 and x < 18:
        plot.annotate('$c_{%s}$' % (x - 5), (x, -0.8), ha='center', size=15)
    if x > 21 and x < 34:
        plot.annotate('$c_{%s}$' % (x - 9), (x, -0.8), ha='center', size=15)

for (x, i) in zip(range(6, 16, 4), range(1, DIM, 2)):
    plot.annotate("$r_{%s}$" % i, (x + 1.5, -1.0),
                  (x + 1.5, -2.1),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,widthB=2.7',
                                  fc="w", ec="k"))

for (x, i) in zip(range(8, 16, 4), range(2, DIM, 2)):
    plot.annotate("$r_{%s}$" % i, (x + 1.5, 0.4),
                  (x + 1.5, 1.4),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,widthB=2.7',
                                  fc="w", ec="k"))

for (x, i) in zip(range(22, 33, 4), range(6, DIM, 2)):
    plot.annotate("$r_{%s}$" % i, (x + 1.5, -1.0),
                  (x + 1.5, -2.1),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,lengthB=0.1,widthB=2.7',
                                  fc="w", ec="k"))

for (x, i) in zip(range(24, 31, 4), range(7, DIM, 2)):
    plot.annotate("$r_{%s}$" % i, (x + 1.5, 0.4),
                  (x + 1.5, 1.4),
                  size=15,
                  ha="center", va="center",
                  arrowprops=dict(arrowstyle='-[,widthB=2.7',
                                  fc="w", ec="k"))

for plot in plots:
    plot.set_xlim(-0.5, DIM - 0.5)
    plot.set_ylim(-2.5, 2)
    plot.set_xticks([])
    plot.set_xticks([])
    plot.set_yticks([])
    plot.set_axis_off()

figure.tight_layout()

#figure.show()

pyplot.savefig('../resources/filters.eps')
