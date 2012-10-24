import numpy as np
from matplotlib import pyplot as plt

years = [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012]
anomaly_detection = [32, 24, 21, 30, 35, 30, 29, 34, 69, 83, 102, 118, 104, 137, 165, 195, 180, 243, 263, 359, 443, 673, 828, 1200, 1610, 2200, 2730, 3210, 3880, 4260, 4360, 5160, 4900]
novelty_detection = [3, 4, 3, 2, 5, 4, 2, 7, 6, 12, 12, 20, 18, 30, 42, 47, 59, 103, 140, 235, 200, 262, 323, 453, 505, 604, 690, 815, 895, 995, 1050, 1160, 1140]
outlier_detection = [21, 34, 38, 28, 32, 30, 42, 77, 82, 110, 131, 147, 211, 226, 242, 292, 320, 387, 479, 471, 534, 725, 849, 1130, 1450, 1800, 2120, 2350, 2740, 2950, 3330, 3740, 3700]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(years[:-1], anomaly_detection[:-1], '-k')
ax.plot(years[:-1], novelty_detection[:-1], '--k')
ax.plot(years[:-1], outlier_detection[:-1], ':k')
ax.set_xlim(1980, 2011)
ax.legend(('"Anomaly detection"', '"Novelty detection"', '"Outlier detection"'), loc=2)

plt.show()
