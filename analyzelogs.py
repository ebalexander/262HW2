# E Alexander & E Balkanski
# Mar 2016 CS 262
#
# Reads logs from timescale.py, imports and visualizes data

import numpy as np
import matplotlib.pyplot as plt

# filenames

f1 = './logs5/log1'
f2 = './logs5/log2'
f3 = './logs5/log3'

# open files and put systime and LC vals into array
l1 = np.loadtxt(f1,skiprows=8,usecols=(0,1,3))
l2 = np.loadtxt(f2,skiprows=8,usecols=(0,1,3))
l3 = np.loadtxt(f3,skiprows=8,usecols=(0,1,3))

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
def timescale():
    plt.scatter(l1[:,0],l1[:,1],color='b',s=5,label=ts1) 
    plt.scatter(l2[:,0],l2[:,1],color='g',s=5,label=ts2)
    plt.scatter(l3[:,0],l3[:,1],color='r',s=5,label=ts3)
    plt.xlabel('system time')
    plt.ylabel('LC')
    plt.title('Timescale Simulation')
    plt.legend(loc='lower right',title='Hz')
    plt.show()
    
# length queue
def lengthQueue():
    plt.scatter(l1[:,0],l1[:,2],color='b',s=5,label=ts1) 
    plt.scatter(l2[:,0],l2[:,2],color='g',s=5,label=ts2)
    plt.scatter(l3[:,0],l3[:,2],color='r',s=5,label=ts3)
    plt.xlabel('system time')
    plt.ylabel('Length of Queue')
    plt.title('Length of the Message Queue')
    plt.legend(loc='best',title='Hz')
    plt.show()

# plots maxLC - minLC versus systime
def gaps():

    x1 = [int(l1[0][0])]
    y1 = [l1[0][1]]
    for i in range(len(l1)):
        if int(l1[i][0]) > x1[-1]:
            x1.append(int(l1[i][0]))
            y1.append(l1[i][1])
    
    x2 = [int(l2[0][0])]
    y2 = [l2[0][1]]
    for i in range(len(l2)):
        if int(l2[i][0]) > x2[-1]:
            x2.append(int(l2[i][0]))
            y2.append(l2[i][1])
              
    
    x3 = [int(l3[0][0])]
    y3 = [l3[0][1]]
    for i in range(len(l3)):
        if int(l3[i][0]) > x3[-1]:
            x3.append(int(l3[i][0]))
            y3.append(l3[i][1])
              
    x = []
    y = []
    for i in x1:
        if i in x3 and i in x2:
            yi1 = y1[x1.index(i)]
            yi2 = y2[x2.index(i)]
            yi3 = y3[x3.index(i)]
            x.append(i)
            y.append(max([yi1,yi2,yi3]) - min([yi1,yi2,yi3]) )

    plt.plot(x,y,color='b') 
    plt.xlabel('system time')
    plt.ylabel('maxLC - minLC')
    plt.title('Gaps in the Logical Clock for Hz ' +str(ts1) +", "+str(ts2) +", "+str(ts3))
    plt.show()



# histogram of jump size
def jumpSize():
    plt.clf()
    
    
    h1 = l1[1:,1]-l1[:-1,1]
    h2 = l2[1:,1]-l2[:-1,1]
    h3 = l3[1:,1]-l3[:-1,1]
    
    #remove jumps of size 1
    
    h1 = filter(lambda x: x != 1, h1)   
    h2 = filter(lambda x: x != 1, h2)   
    h3 = filter(lambda x: x != 1, h3)
    
    

    

    plt.hist(h1, alpha=0.3, label=ts1) 
    # make sure no empty lists
    if len(h2) > 1:
        plt.hist(h2, alpha=0.3, label=ts2)
    else:
        plt.hist([[0]], bins = 1, range= (2,2), label=ts2)
    if len(h3) > 1:
        plt.hist(h3, alpha=0.3, label=ts3)
    else:
        plt.hist([[0]], bins = 1, range= (2,2), label=ts3)

    
    plt.xlabel('count')
    plt.ylabel('LC jump')
    plt.legend(loc='best',title='Hz')
    plt.title('LC jump hist')
    plt.show()

# show plot
#plt.show()
