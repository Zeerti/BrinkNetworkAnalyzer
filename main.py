import ScanNetwork

if __name__ == "__main__":

	scan = ScanNetwork.ScanNetwork(10) #Created class with 10 threads
	scan._get_IP_From_ARP_Table()

	print (scan.totalIPFound)

	for currentIP in range(scan._get_ipList_Size()):
		scan.primaryQueue.put(lambda currentIP = currentIP: scan._get_Active_IP_Addresses(currentIP))


	scan._startScan()


