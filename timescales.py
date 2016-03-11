# E Alexander & E Balkanski
# Mar 2016 CS 262
#
# Launches 3 processes with different time scales and address spaces.
# They maintain logical clocks and send messages (LC values) to each other.
# System time and LC values are logged for each process.

import socket
import time

from random import randint
from multiprocessing import Process

def listenSocket(listenport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', listenport))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    return conn, addr

def sendSocket(sendport):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('', sendport))
    return s
    
def process(p, timescale,logfilename,listenport1, listenport2, sendport1,sendport2):
    
    msg_queue = []
    
    # set up all sockets for listening and sending messages
    # add some waits so that other processes have time to set up the listening
    # do it in different order to avoid deadlocks
    if p == 1:
        conn1, addr1 = listenSocket(listenport1)
        conn2, addr2 = listenSocket(listenport2)
        time.sleep(2)
        s1 = sendSocket(sendport1)
        s2 = sendSocket(sendport2)    
    
    if p == 2:
        time.sleep(1)
        s1 = sendSocket(sendport1)      
        conn1, addr1 = listenSocket(listenport1)
        conn2, addr2 = listenSocket(listenport2)
        time.sleep(3)
        s2 = sendSocket(sendport2)

    if p == 3:
        time.sleep(2)
        s1 = sendSocket(sendport1)
        conn1, addr1 = listenSocket(listenport1)
        time.sleep(2)
        s2 = sendSocket(sendport2)
        conn2, addr2 = listenSocket(listenport2)
        
    # non-blocking sockets so that we can continue the main loop even
    # if we didn't receive anything
    conn1.setblocking(0)
    conn2.setblocking(0)
    
    # start clocks
    LC = 0
    now = time.time()
    
    # start logfile, write header
    logfile = open(logfilename,'w',False) # 'a' to append, False on buffering means immediate write
    logfile.write('Timescale:' + str(timescale) + '\n' +
                  'Ops:' + '\n' +
                  '0' + ' receive' + '\n' +
                  '1' + ' send to neighbor 1' + '\n' +
                  '2' + ' send to neighbor 2' + '\n' +
                  '3' + ' send to both neighbors' + '\n' +
                  '4-10' + ' no-op' + '\n' +
                  '*************************************** \n')
                  
    # run
    while True:
        ##threading.Event.wait.
        # wait to enforce timescale
        ##threading.wait_for(recieve or (time.time()>(now+1/timescale)), timeout=1/timescale)
       
        if int(time.time())>(now+1./timescale):

            now = time.time()

            # check messages
            if len(msg_queue):
                # read message and remove from queue
                senderLC = msg_queue.pop()
                print "MyLC:", LC, "Received:", senderLC
                # update LC
                LC = max(LC,senderLC)+1
                # update log
                logfile.write(str(time.time())+ '\t' + str(LC) + '\t0\n')
            else:
                # randomly select op
                op = randint(1,10)
                # perform pop
                if op==1:
                    # send LC to neigh1
                    s1.send(str(LC))
                elif op==2:
                    # send LC to neigh2
                    s2.send(str(LC)) 
                elif op==3:
                    # send LC to neigh1 and neigh2
                    s1.send(str(LC))
                    s2.send(str(LC))
                # else: "internal event", no-op

                # update LC
                LC += 1

                # update log
                logfile.write(str(time.time())+ '\t' + str(LC) + '\t' + str(op) + '\n')

        # listen for messages to add to the queue
        try:
            data1 = conn1.recv(1024)
            print "Received:", data1
            if not data1: break
            msg_queue.insert(0,int(data1))
        except:
            pass
        
        try:
            data2 = conn2.recv(1024)
            print "Received:", data2
            if not data2: break
            msg_queue.insert(0,int(data2))
        except:
            pass
        
    conn1.close()
    conn2.close()
    
    
    
# bootstrapping process: makes logs and starts the processes
def main():
    # set timescales
    ts1 = 1#randint(1,6)
    ts2 = 2#randint(1,6)
    ts3 = 4#randint(1,6)
    print ts1, ts2, ts3

    # make logfile names
    log1 = './logs/log1'
    log2 = './logs/log2'
    log3 = './logs/log3'

    # ports for sockets 
    port1to2 = 4831
    port1to3 = 5648
    port2to1 = 6833
    port2to3 = 7831
    port3to1 = 8648
    port3to2 = 9833
   
    # make and start processes
    p1 = Process(target=process,args=(1,ts1,log1,port2to1,port3to1,port1to2,port1to3))
    p2 = Process(target=process,args=(2,ts2,log2,port1to2,port3to2,port2to1,port2to3))
    p3 = Process(target=process,args=(3,ts3,log3,port1to3,port2to3,port3to1,port3to2))
    p1.start()
    p2.start()
    p3.start()

main()