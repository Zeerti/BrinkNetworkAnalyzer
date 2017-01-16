#Get ARP Table - DONE
#Ping lists - DONE
#Check open ports on ping replies - high
	#Assume if brink admin port is closed -- Network printer ((Need to check validity of this))- high
	#Port checking NEEDS to be threaded. - high
	#Ping checking NEEDS to be threaded. - high
#Check against known open ports to determine device type. May consider doing MAC checking - high
#Create GUI (tkinter) - low
	#Add in network map - low
#Convert .py to .exe ((PyInstaller-3.2.1)) - medium



#import threading
#import sys
import os
import re
import subprocess
#import socket

ipList = list() #List of IP Address found on ARP Table
regExpFindIPAddress =  re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
arpLines = os.popen('arp -a') #Runs ARP CMD, saves results
totalIPFound = None
pingPass = 0


for lines in arpLines: #Store IP Address out of each line // ADD IN REGULAR EXPRESSION TO STORE IF DYNAMIC OR STATIC IP
	ipMatch = regExpFindIPAddress.search(lines)
	if ipMatch:
		ipList.append(ipMatch.group())

totalIPFound = len(ipList) #Debug Purposes

for currentIP in range(len(ipList)): #Ping each IP found to determine if connected to network // NEED TO ADD THREADING TO IMPROVE PERFORMANCE
	res = subprocess.Popen(['ping', '-n', '1', ipList[currentIP]])
	streamdata = res.communicate()[0]
	rc = res.returncode

	if rc == 0: #Good Ping
		pingPass += 1
	elif rc == 2: #No reply from host
		ipList.pop(currentIP)		
	else: #General Failure to ping
		ipList.append("CRITICAL PING FAILURE")

print("{} Successful pings out of {} found on ARP Table. {} Queries Unknown".format(pingPass, totalIPFound, (totalIPFound-pingPass)))
print(ipList)





 

"""
import socket
import subprocess
import sys
from datetime import datetime

#subprocess.call('clear', shell=True)

remoteServer = '***brinkAdminPortal***'
remoteServerIP = socket.gethostbyname(remoteServer)


try:
	for port in range(port1, port2):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		result = sock.connect_ex((remoteServerIP, port))
		if result == 0:
			print(sock.getpeername())
			print("Port {}:  Open".format(port))
		sock.close()

except KeyboardInterrupt:
	print("You pressed Ctrl+C")
	sys.exit()

except socket.gaierror:
	print('Hostname could not be resolved. Exiting')
	sys.exit()

except socket.error:
	print("Couldn't connect to server")
	sys.exit()

print("Scanning Completed")
"""

#mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s).groups()[0]




