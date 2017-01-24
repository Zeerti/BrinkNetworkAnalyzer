import ScanNetwork

if __name__ == "__main__":

	scan = ScanNetwork.ScanNetwork(5) #Create class, pass number of threads
	scan._get_IP_From_ARP_Table()

	#Add ping scan function to queue
	for currentIP in range(scan._get_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP: scan._get_Active_IP_Addresses(currentIP))
		
	#Run through current queue
	scan._startScan()
	scan.primaryQueue.join() #Wait until _startScan() has finished 

	#Add port scanning to queue
	#for currentIP in range(scan._get_ipList_Size()):
	#	scan.primaryQueue.put(lambda currentIP = currentIP: scan._Scan_IP_Ports(currentIP))

	#Test port scanning
	scan._scan_port(scan.activeIPList[0], 80)
	

	print ("{} active IP Addresses".format(scan._get_active_ipList_Size()))



