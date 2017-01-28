#Get IP addresses in ARP table
#Ping ARP IP and Determine live ip addresses
#	-Add all to the queue using _get_active_ip_addresses(iter)


import queue
import threading
import socket
from threading import Thread
import re
import os
import subprocess

class ScanNetwork():
	def __init__(self, max_Threads):
		self.ipList = list() #List of IP Address found on ARP Table
		self.activeIPList = list()
		self.knownRegisterList = list()
		
		self.totalIPFound = 0
		self.pingPass = 0

		self.totalJobsCompleted = 0
	
		self.primaryQueue = queue.Queue(maxsize=0)
		self.num_threads = max_Threads

	#get queue task
	def do_stuff(self, primaryQueue):
		while True:
			currentOperation = self.primaryQueue.get()
			currentOperation()
			self.totalJobsCompleted += 1
			#print("Completed {} queue Jobs".format(self.totalJobsCompleted))
			self.primaryQueue.task_done()


	#get list of active ip addresses (IP's that have been pinged)
	def _get_Active_IP_Addresses(self, currentIPIteration):
		cmdCommand = subprocess.Popen(['ping', '-n', '1', self.ipList[currentIPIteration]])
		streamdata = cmdCommand.communicate()[0]
		cmdReturnCode = cmdCommand.returncode
		#print("\n\n\nJob# {}, Return Code {}".format(currentIPIteration, cmdReturnCode))

		if cmdReturnCode == 0:
			self.activeIPList.append(self.ipList[currentIPIteration])
		elif cmdReturnCode == 1: #No reply from host
			pass	
		elif cmdReturnCode == 3: #General Failure to ping
			pass

	def _get_IP_From_ARP_Table(self): #Regular Expression Pulls IP Addresses out from ARP Table
		arpLines = os.popen('arp -a') #Runs ARP CMD, saves results into memory
		regExpFindIPAddress =  re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

		for lines in arpLines: #Process saved results from arpLines
			ipMatch = regExpFindIPAddress.search(lines)

			if ipMatch:
				self.ipList.append(ipMatch.group())
				self.totalIPFound += 1

	#Create threads and start them working the queue
	def _startScan(self):
		for i in range(self.num_threads):
			worker = Thread(target=self.do_stuff, args=(self.primaryQueue,)) #target is the function that pops off queue args = arguments for queue function
			worker.setDaemon(True)
			worker.start()

	def _Scan_IP_Port(self, address, port):
		# Create a TCP socket
		socketConnection = socket.socket()
		#print ("Attempting to connect to {} on port {}".format(self.activeIPList[address], port))
		try:
			socketConnection.connect((self.activeIPList[address], port)) #Double Parenthesis needed as it takes a single touple for paramaters 
			#print ("IP {} successfully opened port {}".format(self.activeIPList[address], port))
			self.knownRegisterList.append(self.activeIPList[address])
			return True
		except socket.error:
			#print ("IP {} failed to open port {}".format(self.activeIPList[address], port))
			return False



	def _get_ipList_Size(self):
		return len(self.ipList)

	def _get_active_ipList_Size(self):
		return len(self.activeIPList)

	

	




	

