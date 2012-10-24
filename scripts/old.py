import numpy as np
import math
import pylab

N = 256
T = range(N)
P = 4.5
data = [[math.sin(2*P*math.pi/N * t) for t in T] for i in range(3)]
contextual_collective = []
for t in range(N):
    A = 0.6 if (t < 64 or 128-6.4 < t < 128+6.4 or 192 < t) else 0.2
    contextual_collective.append(A * math.sin(2*20*math.pi/N * t))

data.append(contextual_collective)

#center = (2*P+1)/(4.0*P)*N
center = 128

data[0][int(center)]=1.3
data[1][int(center)]=0
start = int(center - 10)
stop = int(center + 10)
for i in range(start, stop):
    t = 2*math.pi*(i - start) / float(stop - start-1) - math.pi/2
    data[2][i]-=(math.sin(t)+1)/3

fig = pylab.figure()
#fig.subplots_adjust(0.01,-.04,0.99,0.95)
pylab.axis('off')
font = {
        'weight' : 'normal',
        'size'   : 10}
pylab.rc('font', **font)
plots = map(lambda x: fig.add_subplot(4,1,x), range(1,5))

plots[0].set_title('Point anomaly')
plots[1].set_title('Contextual anomaly')
plots[2].set_title('Collective anomaly')
plots[3].set_title('Contextual collective anomaly')
map(lambda x: plots[x].plot(T, data[x], 'k'), range(4))
#map(lambda x: plots[x].scatter(T, data[x], marker='.'), range(4))
map(lambda x: x.set_frame_on(False), plots);
map(lambda x: x.set_xticks([]), plots);
map(lambda x: x.set_yticks([]), plots);
map(lambda x: x.set_ybound(-1.2, 1.5), plots);
map(lambda x: x.set_xbound(-1, N), plots);

fig.tight_layout()

fig.show()
pylab.savefig('../resources/types_of_anomalies.eps')
