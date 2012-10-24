import numpy
import math
import pylab

numpy.random.seed(1)
fig = pylab.figure()
font = {
    'weight' : 'normal',
    'size'   : 10
}

pylab.rc('font', **font)

initial_dimension = 100
total_dimensions = 20
N=range(initial_dimension)

plots = map(lambda x: fig.add_subplot(4,1,x), range(1,5))

rv = []

p = 0

for i in N:
    rv.append(p)
    p += numpy.random.normal(0,0.3)

delta = (5 - rv[-1]) / float(initial_dimension)

rv = map(lambda i: rv[i] + delta * i, N)

assert initial_dimension / total_dimensions == initial_dimension / float(total_dimensions)

dimension_reduced = numpy.ones(total_dimensions)
dimension_increment = initial_dimension / total_dimensions
special_N = []
for i in N:
    special_N.append(i)
    if i % dimension_increment == 0 and i > 0:
        special_N.append(i)
    dimension_reduced[i / dimension_increment] += rv[i]
dimension_reduced /= dimension_increment

discretized = map(round, dimension_reduced)
tick_range = range(int(round(min(discretized))),int(round(max(discretized)))+1)
reduced_repeated = numpy.repeat(dimension_reduced, dimension_increment+1)[:-1]
discretized_repeated = numpy.repeat(discretized, dimension_increment+1)[:-1]

symbolic_ticks = numpy.array(range(total_dimensions)) * dimension_increment + dimension_increment/2.0
symbolic_y_labels = map(chr, range(ord('a'), ord('a')+len(tick_range)))
symbolic_x_labels = map(lambda i: symbolic_y_labels[int(i - min(discretized))], discretized)

# real-valued

plots[0].plot(N, rv, color='k')
plots[0].set_title('Original real-valued series')
plots[0].grid(True)

# numerosity reduced

plots[1].set_title('Dimensionality reduced from %s to %s' % (initial_dimension, total_dimensions))
plots[1].plot(special_N, reduced_repeated, color='k')
plots[1].grid(True)

# dimension reduced

plots[2].plot(special_N, discretized_repeated, color='k')
plots[2].set_title('Numerosity reduced through discretization')
#plots[2].set_yticks(tick_range)
plots[2].grid(True)

# discrete symbolic
#plots[3].plot(N, disc, color='k')
plots[3].scatter(symbolic_ticks, discretized, color='k')
plots[3].plot(special_N, discretized_repeated, color='k')
plots[3].set_title('Conversion to symbolic sequence')
plots[3].set_yticks(tick_range)
plots[3].set_yticklabels(symbolic_y_labels)
plots[3].set_xticks(symbolic_ticks)
plots[3].set_xticklabels(symbolic_x_labels)
plots[3].grid(True)

map(lambda x: x.set_xticks([]), plots[0:3])
map(lambda x: x.set_xbound(0, 99), plots)
#map(lambda x: x.set_ybound(min(rv)-0.5, max(rv)+0.5), plots[0:2])
map(lambda x: x.set_ybound(min(tick_range)-1, max(tick_range)+1), plots[2:])

fig.tight_layout()

fig.show()
pylab.savefig('../resources/types_of_data.eps')
