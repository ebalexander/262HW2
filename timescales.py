# E Alexander & E Balkanski
# Mar 2016 CS 262
#
# Launches 3 processes with different time scales and address spaces.
# They maintain logical clocks and send messages (LC values) to each other.
# System time and LC values are logged for each process.

import socket
import time

from random import randint
from threading import Thread
from multiprocessing import Process

def listen(myport,msg_queue):
    # if neigh1 or neigh2 sends a message, add it to msg_queue
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', myport))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        print "Received:", data
        if not data: break
        msg_queue.insert(0,int(data))
    conn.close()

##def processmain
    

def process(timescale,logfilename,listenport1, listenport2, sendport1,sendport2):
    
    # start listening
    msg_queue = []
    
    listen_thread1 = Thread(target=listen,args=(listenport1,msg_queue))
    listen_thread1.start()

    listen_thread2 = Thread(target=listen,args=(listenport2,msg_queue))
    listen_thread2.start()	
    
    # start clocks
    LC = 0
    now = time.time()
    
    # wait for all sockets to be listening
    time.sleep(2)

    #start sockets to send messages
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(('', sendport1))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(('', sendport2))
    
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

# bootstrapping process: makes sockets and logs and starts the processes
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
    port1to2 = 1831
    port1to3 = 2648
    port2to1 = 3833
    port2to3 = 4831
    port3to1 = 5648
    port3to2 = 6833
   
    # make and start processes
    p1 = Process(target=process,args=(ts1,log1,port2to1,port3to1,port1to2,port1to3))
    p2 = Process(target=process,args=(ts2,log2,port1to2,port3to2,port2to1,port2to3))
    p3 = Process(target=process,args=(ts3,log3,port1to3,port2to3,port3to1,port3to2))
    p1.start()
    p2.start()
    p3.start()

main()