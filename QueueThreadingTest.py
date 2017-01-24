#Threading
#Queue
import queue
import threading
from threading import Thread
import re
import os
import subprocess

ipList = list() #List of IP Address found on ARP Table
regExpFindIPAddress =  re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
arpLines = os.popen('arp -a') #Runs ARP CMD, saves results
totalIPFound = None
pingPass = 0



primaryQueue = queue.Queue(maxsize=0)
num_threads = 10


#Function to run through queue
def do_stuff(primaryQueue):
	while True:
		currentOperation = primaryQueue.get()
		#print("Currently Running: {}".format(currentOperation))
		currentOperation()
		primaryQueue.task_done()

def _get_Active_IP_Addresses(currentIPIteration, pingPass):
		#print("Iteration {}".format(currentIPIteration))
		res = subprocess.Popen(['ping', '-n', '1', ipList[currentIPIteration]])
		#print("CMD PINGING: {} ".format(ipList[currentIPIteration]))
		streamdata = res.communicate()[0]
		rc = res.returncode
	
		if rc == 0: #Good Ping
			pingPass += 1
		elif rc == 2: #No reply from host
			ipList.pop(currentIPIteration)		
		else: #General Failure to ping
			pingPass -= 1



for lines in arpLines: #Store IP Address out of each line // ADD IN REGULAR EXPRESSION TO STORE IF DYNAMIC OR STATIC IP
	ipMatch = regExpFindIPAddress.search(lines)
	if ipMatch:
		ipList.append(ipMatch.group())


#add tasks to queue ////////////// DOES NOT NEED FUNCTION TO DO THIS
for currentIP in range(len(ipList)):
	primaryQueue.put(lambda currentIP = currentIP, pingPass = pingPass: _get_Active_IP_Addresses(currentIP, pingPass))



#Loop to create threads, given queue to process
for i in range(num_threads):
	worker = Thread(target=do_stuff, args=(primaryQueue,)) #target is the function that pops off queue args = arguments for queue function
	worker.setDaemon(True)
	worker.start()
	#print("Started Worker {}, Number {}".format(worker, i))



primaryQueue.join()
print(pingPass)



"""
def worker():
	while True:
		item = q.get()
		do_work(item)
		q.task_done()

q = queue.Queue()
for i in range(num_worker_threads):
	t = Thread(target=worker)
	t.daemon = True
	t.start()

for item in source():
	q.put(item)

q.join() #block until all tasks are completed
"""