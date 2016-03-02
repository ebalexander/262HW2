import socket
import time

from random import randint
from threading import Thread
from multiprocessing import Process

msg_queue = []

def listen():
    # if neigh1 or neigh2 sends a message, add it to msg_queue
    ### socket stuff here
    msg_queue.insert(0,senderLC)

def process(timescale,logfilename,mysock,neigh1,neigh2):

    # start logfile
    logfile = open(logfilename,'w') # 'a' to append

    # start listening
    listen_thread = Thread(target=self.listen)
    listen_thread.start()

    # start clocks
    LC = 1
    now = int(time.time())

    # run
    while True:
        # wait to enforce timescale (should maybe do sleeping?)
        if int(time.time())>(now+1/timescale):
            now = int(time.time())

            # check messages
            if len(msq_queue):
                # read message and remove from queue
                senderLC = pop(msg_queue)
                # update LC
                LC = max(LC,senderLC)+1 
            else:
                # randomly select op
                op = randint(1,10)
                # perform pop
                if op==1:
                    # send LC to neigh1
                    ### socket stuff here
                elif op==2:
                    # send LC to neigh2
                    ### socket stuff here  
                elif op==3:
                    # send LC to neigh1 and neigh2
                    ### socket stuff here
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

    # make sockets
    ### I need to read about sockets

    # make and start processes
    p1 = Process(target=process,args=(ts1,log1,sock1,sock2,sock3))
    p2 = Process(target=process,args=(ts2,log2,sock2,sock3,sock1))
    p3 = Process(target=process,args=(ts3,log3,sock3,sock1,sock2))
    p1.start()
    p2.start()
    p3.start()
