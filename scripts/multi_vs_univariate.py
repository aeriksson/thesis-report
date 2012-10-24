import math
import pylab
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d import proj3d

fig = pylab.figure(figsize=[12,8])
fig.subplots_adjust(-0.07,0,1.05,1)
plot = fig.gca(projection='3d')
plot.azim = 110
plot.elev = 20
plot.autoscale(enable=True, tight=True)

w = 0.1
N = 200
T = range(N)
x = [math.sin(w * t) for t in T]
y = [math.cos(w * t) for t in T]
plot.plot(T,x,zs=y, c='k')
m = -1 * np.ones(N)
plot.plot(T, m, zs=y, c='k', linestyle=':')
plot.plot(T, x, zs=m, c='k', linestyle=':')

plot.set_xticks([])
plot.set_yticks([])
plot.set_zticks([])
fig.show()
pylab.savefig('../resources/multi_vs_univariate.eps', bbox_inches='tight', pad_inches=-0.7)
