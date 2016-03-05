import socket
import time

from random import randint
from threading import Thread
from multiprocessing import Process

msg_queue = []

def listen(myport):
    # if neigh1 or neigh2 sends a message, add it to msg_queue
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', myport))
    s.listen(1)
    conn, addr = s.accept()
    print 'Connected by', addr
    while 1:
        data = conn.recv(1024)
        print "Received: " 
        print data
        if not data: break
        msg_queue.insert(0,int(data))
    conn.close()
    

def process(timescale,logfilename,listenport1, listenport2, sendport1,sendport2):
    # start logfile
    logfile = open(logfilename,'w') # 'a' to append

    # start listening
    listen_thread1 = Thread(target=listen,args=(listenport1,))
    listen_thread1.start()

    listen_thread2 = Thread(target=listen,args=(listenport2,))
    listen_thread2.start()
    
    # start clocks
    LC = 1
    now = int(time.time())
    
    # wait for all sockets to be listening
    time.sleep(2)

    #start sockets to send messages
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect(('', sendport1))
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.connect(('', sendport2))
    
    # run
    while True:
        # wait to enforce timescale (should maybe do sleeping?)
        if int(time.time())>(now+1/timescale):
            now = int(time.time())

            # check messages
            if len(msg_queue):
                # read message and remove from queue
                senderLC = msg_queue.pop()
                # update LC
                LC = max(LC,senderLC)+1 
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
        ### unclear what this will look like ###
        # should possibly go inside if/else
        logfile.write('log string \n')

def main():
    # set timescales
    ts1 = randint(1,6)
    ts2 = randint(1,6)
    ts3 = randint(1,6)

    # make logfile names
    log1 = './.logs/log1'
    log2 = './.logs/log2'
    log3 = './.logs/log3'

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