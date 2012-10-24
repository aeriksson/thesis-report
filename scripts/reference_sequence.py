import numpy
import math
import pylab

(sequence, anomaly_vector) = numpy.load('random_walk_added_noise')

fig = pylab.figure()
pylab.axis('off')
font = {
        'weight' : 'normal',
        'size'   : 10}
pylab.rc('font', **font)
plots = map(lambda x: fig.add_subplot(2,1,x), range(1,3))

plots[0].set_title('Sequence')
plots[0].plot(sequence, 'k')

plots[1].plot(anomaly_vector, 'k')
plots[1].set_title('Anomaly vector')

plots[1].set_ylim([-0.1, 1.1])

plots[0].set_yticks([])
plots[1].set_yticks([])

fig.set_figheight(4)
fig.tight_layout()

fig.set_size_inches(8.125, 4.1)

pylab.savefig('../resources/reference_sequence.eps')
