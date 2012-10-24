import math
import pylab
import numpy

numpy.random.seed(2)

font = {
    #'family': 'normal',
    'weight': 'normal',
    'size': '10'
    }
pylab.rc('font', **font)
pylab.axis('equal')
pylab.ion()

N = 1000
phis = pylab.rand(N) * 2 * math.pi
rs = pylab.randn(N) * 0.1 + 1
rs[-1] = 0
xs = [r * math.cos(phi) for (r,phi) in zip(rs, phis)]
ys = [r * math.sin(phi) for (r,phi) in zip(rs, phis)] 

xs.append(0)
ys.append(0)

plots = [
  pylab.subplot2grid((2,2), (0,0), rowspan=2),
  pylab.subplot2grid((2,2), (0,1)),
  pylab.subplot2grid((2,2), (1,1))
]

anomaly_color=(0.5,0.5,1.0)

plots[0].scatter(xs, ys, 2.0, c='k')
plots[0].arrow(0, 0.25, 0.0, -0.1, fc="k", ec="k", head_width=0.05, head_length=0.1)
plots[1].hist(xs, bins= 40, normed=True, color='k', histtype='stepfilled')
plots[1].arrow(0.032, 0.44, 0.0, -0.09, fc="k", ec="k", head_width=0.04, head_length=0.06)
plots[2].hist(rs, bins= 40, normed=True, color='k', histtype='stepfilled')
plots[2].arrow(0.018, 0.6, 0.0, -0.3, fc="k", ec="k", head_width=0.02, head_length=0.2)
plots[2].set_xlim([-0.1,1.4])

plots[0].set_title('Scatter plot of multivariate data')
plots[1].set_title('Histogram of one component of multivariate data')
plots[2].set_title('Histogram of distance from center') 

map(lambda x: x.set_xticks([]), plots)
map(lambda x: x.set_yticks([]), plots)

pylab.tight_layout()

#pylab.savefig('../resources/multivariate.eps')
