# BrinkNetworkAnalyzer
Analyze Brink Networks for Devices Connected to Network

###Future Features###
- [x] Get IP Addresses from ARP Table
- [x] Ping IP Addresses from ARP Table
- [x] Create GUI
- [x] Threading for pinging and port scanning
- [x] Convert script to x64 exe for portability (PyInstaller-3.2.1)
- [ ] Full ping sweep of various network sizes as a GUI option
- [ ] Device identification based on findings
- [ ] Convert script to x32 exe for portability (PyInstaller-3.2.1)
- [ ] Add in icons for discovered IP addresses to display what device found was
- [ ] Add in progress bar when performing any scans
- [ ] Transpose all findings to a file, possibly XML?
- [ ] Create custom header Renderer to change appearance of headers to match GUI mockup


###How to Use###
Start with a Scan -> Scan All

Select an IP Address

Scan -> Port Scan

Will put a full list of open ports in the detailed window view

###Bugs###

- [x] Port Scanning seems to be failing constantly (Unable to locate target host)
- [ ] Index problems with ipULC -- Last ip in list is off by one unless there is a large list


