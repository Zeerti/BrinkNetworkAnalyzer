import scan

port = 10051

if __name__ == "__main__":

	scan = scan.ScanNetwork(10) #Create class, pass number of threads
	scan._get_IP_From_ARP_Table()# Scrape IPs from ARP Table

	#Add ping function to queue
	for currentIP in range(scan._get_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP: scan._get_Active_IP_Addresses(currentIP))
		
	#Run through current queue (Ping each IP scraped)
	scan._startScan()
	scan.primaryQueue.join() #Wait until done pinging all IP addresses 

	#Add port scanning to queue
	#Check Port 80 for testing, eventually check 10051
	for currentIP in range(scan._get_active_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP, port = port: scan._Scan_IP_Port(currentIP, port))

	scan._startScan()
	scan.primaryQueue.join() #wait until all IPs have been scanned on port, port.

	print("\n\nPort {} open for the following IP Addresses".format(port))

	for iteration in range(len(scan.knownRegisterList)): #Print out list of all IP Address with port, 'port' open.
		print(scan.knownRegisterList[iteration])

	



