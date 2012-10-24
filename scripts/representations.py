import numpy
import math
import pylab
import pywt

numpy.random.seed(1)
fig = pylab.figure()
font = {
    'weight' : 'normal',
    'size'   : 10
}

pylab.rc('font', **font)

N=range(100)

plots = map(lambda x: fig.add_subplot(1,4,x), range(1,5))

# original series
rv = []

p = 0

for i in N:
    rv.append(p)
    p += numpy.random.normal(0,0.3)

# haar wavelet
plots[0].plot(N, rv, color='k')
plots[0].set_title('Real-valued time series') 

signals = map(lambda x: pywt.wavedec(rv, 'haar', level=x), range(1,10))
for s in signals:
    print s
    pylab.plot(pywt.waverec(s,'haar'))

pylab.show()


#disc = map(round, rv)
#
#plots[1].plot(N, disc, color='k')
#plots[1].set_title('Discrete numerical time series')
#plots[1].set_yticks(range(-2,3))
#plots[1].grid(True)
#
## discrete symbolic
#plots[2].plot(N, disc, color='k')
#plots[2].set_title('Discrete symbolic time series')
#plots[2].set_yticks([-2, -1, 0, 1, 2])
#plots[2].set_yticklabels(['a', 'b', 'c', 'd', 'e'])
#plots[2].grid(True)
#
#map(lambda x: x.set_xticks([]), plots)
#map(lambda x: x.set_xbound(0, 99), plots)
#map(lambda x: x.set_ybound(-2.5, 2.5), plots)
#
#fig.tight_layout()
#
#fig.show()
#pylab.savefig('../resources/types_of_data.eps')
