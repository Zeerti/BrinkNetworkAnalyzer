import ScanNetwork

port = 80

if __name__ == "__main__":

	scan = ScanNetwork.ScanNetwork(10) #Create class, pass number of threads
	scan._get_IP_From_ARP_Table()

	#Add ping scan function to queue
	for currentIP in range(scan._get_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP: scan._get_Active_IP_Addresses(currentIP))
		
	#Run through current queue
	scan._startScan()
	scan.primaryQueue.join() #Wait until _startScan() has finished 

	#Add port scanning to queue
	#Check Port 80 for testing, eventually check 10051

	for currentIP in range(scan._get_active_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP, port = port: scan._Scan_IP_Port(currentIP, port))

	scan._startScan()
	scan.primaryQueue.join()

	print(scan.knownRegisterList)

	#Test port scanning
	#scan._scan_port(scan.activeIPList[0], 80)
	



