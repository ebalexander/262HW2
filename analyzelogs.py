# E Alexander & E Balkanski
# Mar 2016 CS 262
#
# Reads logs from timescale.py, imports and visualizes data

import numpy as np
import matplotlib.pyplot as plt

# filenames
f1 = './logs/log1'
f2 = './logs/log2'
f3 = './logs/log3'

# open files and put systime and LC vals into array
l1 = np.loadtxt(f1,skiprows=8,usecols=(0,1))
l2 = np.loadtxt(f2,skiprows=8,usecols=(0,1))
l3 = np.loadtxt(f3,skiprows=8,usecols=(0,1))

# read timestamps
with open(f1, 'r') as handle:
    first_line = handle.readline()
    ts1 = first_line[10]
with open(f2, 'r') as handle:
    first_line = handle.readline()
    ts2 = first_line[10]
with open(f3, 'r') as handle:
    first_line = handle.readline()
    ts3 = first_line[10]

# plot each process's LC versus systime
plt.subplot(3,1,1)
plt.scatter(l1[:,0],l1[:,1],color='b',label=ts1) #should label with timescale
plt.scatter(l2[:,0],l2[:,1],color='g',label=ts2)
plt.scatter(l3[:,0],l3[:,1],color='r',label=ts3)
plt.xlabel('system time')
plt.ylabel('LC')
plt.title('Timescale Simulation')
plt.legend(loc='best',title='Hz')

# plot max(LC)-min(LC) over time, as hist
plt.subplot(2,3,4)
## TODO
plt.xlabel('plot')
plt.ylabel('LC gap')
plt.title('LC gap hist, coming soon')

# histogram of jump size
plt.subplot(2,3,6)
plt.hist(l1[1:,1]-l1[:-1,1], alpha=0.3, label=ts1) #should label with timescale
plt.hist(l2[1:,1]-l2[:-1,1], alpha=0.3, label=ts2)
plt.hist(l3[1:,1]-l3[:-1,1], alpha=0.3, label=ts3)
plt.xlabel('count')
plt.ylabel('LC jump')
plt.legend(loc='best',title='Hz')
plt.title('LC jump hist')

# show plot
plt.show()
