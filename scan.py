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
from subprocess import Popen, PIPE

class ScanNetwork():
	def __init__(self, max_Threads):
		self.nodes = {} #Where we store all the information gathered on ip addresses
		self.ipList = list() #List of IP Address found on ARP Table ||||||| STILL IN USE
		#self.pingStatistics = list()
		#self.activeIPList = list()
		#self.openPortList = list() #Stores all open Ports for a --SINGLE-- ipadress MUST BE CLEARED BEFORE REUSING
		
		self.totalIPFound = 0
		self.primaryQueue = queue.Queue(maxsize=0)
		self.num_threads = max_Threads

	#----------------------------------------------------------------------
	#get queue task
	def do_stuff(self, primaryQueue):
		while True:
			currentOperation = self.primaryQueue.get()
			currentOperation()
			self.primaryQueue.task_done()


	#----------------------------------------------------------------------
	#get list of active ip addresses (IP's that have been pinged)
	def _get_Active_IP_Addresses(self, currentIPIteration):
		cmdCommand = Popen(['ping', '-n', '1', self.ipList[currentIPIteration]], stdout=PIPE)
		text = cmdCommand.communicate()[0]
		cmdReturnCode = cmdCommand.returncode

		if cmdReturnCode == 0:
			#self.pingStatistics.append(text)
			#####self.activeIPList.append(self.ipList[currentIPIteration])
			self.nodes[self.ipList[currentIPIteration]] = {'mac':'UNKNOWN',
															'ping':'UNKNOWN',
															'ports':'UNKNOWN',
															'gateway':'UNKNOWN', 
															'device':'UNKNOWN'}
			self.nodes[self.ipList[currentIPIteration]]['ping'] = text
		elif cmdReturnCode == 1: #No reply from host
			pass	
		elif cmdReturnCode == 3: #General Failure to ping
			pass

	#----------------------------------------------------------------------
	def _get_IP_From_ARP_Table(self): #Regular Expression Pulls IP Addresses out from ARP Table
		arpLines = os.popen('arp -a') #Runs ARP CMD, saves results into memory
		regExpFindIPAddress =  re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')

		for lines in arpLines: #Process saved results from arpLines
			ipMatch = regExpFindIPAddress.search(lines)

			if ipMatch:
				self.ipList.append(ipMatch.group())
				self.totalIPFound += 1

	#----------------------------------------------------------------------
	#Create threads and start them working the queue
	def _startScan(self):
		for i in range(self.num_threads):
			worker = Thread(target=self.do_stuff, args=(self.primaryQueue,)) #target is the function that pops off queue args = arguments for queue function
			worker.setDaemon(True)
			worker.start()

	

	#----------------------------------------------------------------------
	def _Scan_IP_Port(self, address, port):
		# Create a TCP socket
		socketConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketConnection.settimeout(10)
		HOST = str(address)
		TempPort = port
		#print ("Attempting to connect to {} on port {}".format(self.activeIPList[address], port))
		try:
			socketConnection.connect((HOST, TempPort)) #Double Parenthesis needed as it takes a single touple for paramaters 
			#self.openPortList.append("{} ||".format(TempPort))
			
			if self.nodes[str(address)]['ports'] == 'UNKNOWN': #Ports have not been set.
				self.nodes[str(address)]['ports'] = str(TempPort)
			else:
				self.nodes[str(address)]['ports'] = self.nodes[str(address)]['ports'] + '||' + str(TempPort)

			return True
		except socket.error as err:
			print ("IP {} failed to open port {}, ERROR: {}".format(HOST, TempPort, err))
			socket.error()
			return False

	#----------------------------------------------------------------------
	def _resetIPList(self):
		del self.ipList[:]
		self.totalIPFound = 0															

	#----------------------------------------------------------------------
	#def _resetPingStatisticsList(self):
	#	del self.pingStatistics[:]
		
	#----------------------------------------------------------------------
	def _resetActiveIPList(self):
		del self.activeIPList[:]

	#----------------------------------------------------------------------
	def _resetOpenPortList(self):
		del self.openPortList[:]

	#----------------------------------------------------------------------
	def _get_ipList_Size(self):
		return len(self.ipList)

	#----------------------------------------------------------------------
	def _get_Open_Ports(self, iteration):
		return self.openPortList[iteration]

	#----------------------------------------------------------------------
	def _get_Open_Ports_Size(self):
		return len(self.openPortList)

	#----------------------------------------------------------------------
	def _get_active_ipList_Size(self):
		return len(self.activeIPList)

	#----------------------------------------------------------------------
	#def _Get_Ping_Statistics(self, iteration):
	#	return self.pingStatistics[iteration]

	

	




	

