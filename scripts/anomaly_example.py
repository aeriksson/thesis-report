import numpy as np
import math
import pylab
import random

random.seed(1)

N = 500

data = []
for t in range(N):
    amplitude = 1.5 if t in range(245, 255) else 0.2
    data.append(random.gauss(0,amplitude))

fig = pylab.figure(figsize=(16, 4))
pylab.axis('off')
font = {
        'weight' : 'normal',
        'size'   : 10}
pylab.rc('font', **font)
plot = fig.gca()

plot.plot(data, 'k')

plot.set_xticks([])
plot.set_yticks([])

fig.tight_layout()

fig.show()
pylab.savefig('../resources/anomaly_example.eps')
