import numpy as np
import math
import pylab

N = 512
T = range(N)
P = 20
#data = [[P * math.sin(P*math.pi/N * t) for t in T] for i in range(2)]
data = [[0.6 * math.sin(2*P*math.pi/N * t) for t in T]]
data.append([0.6 * math.sin(2*P*math.pi/N * t) + float(t - N / 2) * (t - N / 2) / N / N * 5.0 - 0.5 for t in T])
center = N/2

collective = []
collective_anomaly = []
COLLECTIVE_ANOMALY_START = int(center - N / 20.0 + 1)
COLLECTIVE_ANOMALY_END = int(center + N / 20.0 + 1)
COLLECTIVE_ANOMALY_INTERVAL = range(COLLECTIVE_ANOMALY_START, COLLECTIVE_ANOMALY_END)
for t in range(N):
    amplitude = 0.6 if not t in COLLECTIVE_ANOMALY_INTERVAL else 0.2
    data_point = amplitude * math.sin(2*20*math.pi/N * t)

    collective.append(data_point)
    if t in COLLECTIVE_ANOMALY_INTERVAL:
        collective_anomaly.append(data_point)

data.append(collective)

contextual_collective = []
for t in range(N):
    A = 0.6 if not (t < center*0.4 or center-N/20.0 < t < center+N/20.0 or center*1.6 < t) else 0.2
    contextual_collective.append(A * math.sin(2*20*math.pi/N * t))

data.append(contextual_collective)

start = int(center - 10)
stop = int(center + 10)

fig = pylab.figure()
pylab.axis('off')
font = {
        'weight' : 'normal',
        'size'   : 8}
pylab.rc('font', **font)
plots = map(lambda x: fig.add_subplot(4,1,x), range(1,5))

plots[0].set_title('Point anomaly')
plots[1].set_title('Contextual point anomaly')
plots[2].set_title('Collective anomaly')
plots[3].set_title('Contextual collective anomaly')

plots[0].plot(T, data[0], color='0.6', linewidth=2)
#plots[0].scatter([center], [1], linewidth=2, marker='.', c='r')
plots[0].scatter([center], [1], s=50, c='k', marker='.', edgecolors='none')
POINT_ANOMALY_INTERVAL = range(center-3,center+3)
#plots[0].plot(POINT_ANOMALY_INTERVAL, [-1.1] * len(POINT_ANOMALY_INTERVAL), 'k', linewidth=4)

CONTEXT_WIDTH = 100
plots[1].plot(T[:center-CONTEXT_WIDTH + 1], data[1][:center-CONTEXT_WIDTH + 1], color='0.9', linewidth=2)
plots[1].plot(T[center-CONTEXT_WIDTH:center+CONTEXT_WIDTH], data[1][center-CONTEXT_WIDTH:center+CONTEXT_WIDTH], color='0.6', linewidth=2)
plots[1].plot(T[center+CONTEXT_WIDTH - 1:], data[1][center+CONTEXT_WIDTH - 1:], color='0.9', linewidth=2)
plots[1].scatter([center], [0.6], s=50, marker='.', c='k', edgecolors='none')
#plots[1].plot(POINT_ANOMALY_INTERVAL, [-1.1] * len(POINT_ANOMALY_INTERVAL), 'k', linewidth=4)

plots[2].plot(T[:COLLECTIVE_ANOMALY_START+1], data[2][:COLLECTIVE_ANOMALY_START+1], color='0.6', linewidth=2)
plots[2].plot(T[COLLECTIVE_ANOMALY_END-1:], data[2][COLLECTIVE_ANOMALY_END-1:], color='0.6', linewidth=2)
plots[2].plot(COLLECTIVE_ANOMALY_INTERVAL, collective_anomaly, 'k', linewidth=2)
#plots[2].plot(COLLECTIVE_ANOMALY_INTERVAL, collective_anomaly, 'k', linewidth=4)
#plots[2].plot(COLLECTIVE_ANOMALY_INTERVAL, [-1.1] * len(COLLECTIVE_ANOMALY_INTERVAL), 'k', linewidth=4)

CONTEXT_WIDTH = 100
plots[3].plot(T[:center-CONTEXT_WIDTH], data[3][:center-CONTEXT_WIDTH], color='0.9', linewidth=2)
plots[3].plot(T[center+CONTEXT_WIDTH:], data[3][center+CONTEXT_WIDTH:], color='0.9', linewidth=2)
plots[3].plot(T[center-CONTEXT_WIDTH - 1:COLLECTIVE_ANOMALY_START + 1], data[3][center-CONTEXT_WIDTH - 1:COLLECTIVE_ANOMALY_START + 1], color='0.6', linewidth=2)
plots[3].plot(T[COLLECTIVE_ANOMALY_END - 1:center+CONTEXT_WIDTH + 1], data[3][COLLECTIVE_ANOMALY_END - 1:center+CONTEXT_WIDTH + 1], color='0.6', linewidth=2)
plots[3].plot(COLLECTIVE_ANOMALY_INTERVAL[:-1], [contextual_collective[i] for i in COLLECTIVE_ANOMALY_INTERVAL[:-1]], color='0', linewidth=2)
#plots[3].plot(COLLECTIVE_ANOMALY_INTERVAL, [-1.1] * len(COLLECTIVE_ANOMALY_INTERVAL), 'k', linewidth=4)

map(lambda x: x.set_frame_on(False), plots);
map(lambda x: x.set_xticks([]), plots);
map(lambda x: x.set_yticks([]), plots);
map(lambda x: x.set_ybound(-1.2, 1.5), plots);
map(lambda x: x.set_xbound(-1, N), plots);

fig.tight_layout()

fig.show()
pylab.savefig('../resources/types_of_anomalies.eps')
