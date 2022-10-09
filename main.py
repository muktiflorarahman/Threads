#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# Namn: Mukti Flora Rahman
# Kurs: Operativsystem
# Labb: Trådar 
# Datum: 2022-10-09

# Lösning på Readers-Writers problem

import threading
import time
from threading import Semaphore

readCount = 0
readMutex = Semaphore(value=3)
readTry = Semaphore(value=3)
resourceSemaphore = Semaphore()
resource = "2022-10-09"

def readVar(name):
    global resource
    print(name, "is reading... -", resource)

#    //READER
def readerOfFile(sleep, name):
    global readCount
    global readMutex
    global readTry

# <ENTRY Section>
    while readCount < 1000:
        readTry.acquire()
        readMutex.acquire()
        readCount += 1
        
        if readCount == 1:
            resourceSemaphore.acquire()
        readMutex.release()
        readTry.release()

#CRITICAL SECTION
        readVar(name)
    
            
        
#EXIT SECTION
        readMutex.acquire()
        readCount -= 1
        if readCount == 0:
            resourceSemaphore.release()
        readMutex.release()
        readCount += 1
        time.sleep(sleep)

        
        


def main():
    # skapar 3 lästrådar
    for reader in range(3):
        readerThread = threading.Thread(target = readerOfFile,
        name = f'Reader - {reader}',
        args = (0, f'Reader - {reader}'))
        readerThread.start()


if (__name__ == '__main__'):
    main()