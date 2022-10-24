#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# Namn: Mukti Flora Rahman
# Kurs: Operativsystem
# Labb: Trådar 
# Datum: 2022-10-09

# Lösning på Readers-Writers problem

import threading
# from threading import Lock
from threading import Semaphore
import time
import datetime

nrWritersCor = 0
nrWritersRev = 0
nrOfReaders = 0
rmutex = Semaphore()
wmutex = Semaphore()
readTry = Semaphore()
resourceSem = Semaphore()
writeCount = 0
readCount = 0
resource = ""

def timeStamp(isCorrectStamp):
  now = datetime.datetime.now()
  dateStamp = now.strftime("%Y-%m-%d %H:%M:%S")
  pmatSetad = ''.join(reversed(dateStamp))

  if isCorrectStamp:
    return 'Correct  stamp: ' + dateStamp
  else:
    return 'Reversed stamp: ' + pmatSetad

def writeToVar(name, text):
	global resource
	resource = text
	print('{} is writing... - {}'.format(name, resource))


def readVar(name):
	global resource
	print(name, "is reading... -", resource)


def readerOfFile(n, name):
	global resourceSem
	global readTry
	global rmutex
	global readCount
	global nrOfReaders

	# ENTRY SECTION
	while (nrOfReaders < 1000):
		readTry.acquire()
		rmutex.acquire()
		readCount += 1
		if (readCount == 1):
			resourceSem.acquire()
		rmutex.release()
		readTry.release()

	# CRITICAL SECTION
		readVar(name)

	# EXIT SECTION
		rmutex.acquire()
		readCount -= 1
		if (readCount == 0):
			resourceSem.release()
		rmutex.release()
		nrOfReaders += 1
		time.sleep(n)


def writerToCorrect(n, name):
	global resourceSem
	global wmutex
	global nrWritersCor
	global writeCount

	# ENTRY SECTION # thread blocks at this line until it can obtain lock
	while (nrWritersCor < 1000):
		wmutex.acquire()
		writeCount += 1
		if (writeCount == 1):
			readTry.acquire()
		wmutex.release()

	# CRITICAL SECTION
		resourceSem.acquire()
		writeToVar(name, timeStamp(True))
		resourceSem.release()

	# EXIT SECTION
  # in this section,
  # only one thread can be present at a time.
		wmutex.acquire()
		writeCount -= 1
		if (writeCount == 0):
			readTry.release()
		wmutex.release()
		nrWritersCor += 1
		time.sleep(n)


def writerToReverse(n, name):
	global resourceSem
	global wmutex
	global nrWritersRev
	global writeCount

	# ENTRY SECTION # thread blocks at this line until it can obtain lock
	while (nrWritersRev < 1000):
		wmutex.acquire()
		writeCount += 1
		if (writeCount == 1):
			readTry.acquire()
		wmutex.release()

	# CRITICAL SECTION
		resourceSem.acquire()
		writeToVar(name, timeStamp(False))
		resourceSem.release()

	# EXIT SECTION # in this section, only one thread can be present at a time.
		wmutex.acquire()
		writeCount -= 1
		if (writeCount == 0):
			readTry.release()
		wmutex.release()
		nrWritersRev += 1
		time.sleep(n)


def main():
  # skapar 3 lästrådar
    #skapar readerThread med olika argument
    # sätter igång readerThread
	for re in range(3):
		rt = threading.Thread(target = readerOfFile,
      name = 'Reader{}'.format(re),
      args = (0, 'Reader{}'.format(re)))
		rt.start()

#skapar läsartråd 1
#Skriver en datumstämpel, inklusive sekunder till textsträngen
	wct = threading.Thread(target = writerToCorrect,
    name = 'Writer_cor',
    args = (0, 'Writer_cor'))
	wct.start()

  #skapar 1 skrivartråd 2
  #Skriver ut omvänd datumstämpel
	wrt = threading.Thread(target = writerToReverse,
    name = 'Writer_rev',
    args = (0, 'Writer_rev'))
	wrt.start()


if (__name__ == '__main__'):
	main()
    