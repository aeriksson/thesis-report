import numpy as np
import matplotlib.pyplot as plt

b = np.cumsum(np.concatenate([np.random.exponential(1, 600), np.random.exponential(0.5, 100), np.random.exponential(1,200)]))

fig = plt.figure()
plots = map(lambda x: fig.add_subplot(5,1,x), range(1,6))
map(lambda x, i: x.hist(b, i, histtype='stepfilled', color='black'), plots, (192, 96, 48, 24, 12));
map(lambda x: x.set_xbound(min(b), max(b)), plots);
map(lambda x: x.set_xticks([]), plots);
map(lambda x: x.set_yticks([]), plots);
fig.show()
