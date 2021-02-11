#!/usr/bin/env python3

import argparse
from scapy.all import *
import subprocess
import os
import sys
import random

def module_name():
	return "quiet-port-scanner"

def module_help():
	return "a quiet port scanner to find open ports on opponents machines"

def module_usage():
	return subprocess.check_output("python3 modules/quiet-port-scanner.py -h", shell=True).decode("utf-8")

def randomPort():
	rand = random.randint(1023,10000)#avoid designated port
	return rand

def SYNScan(ports, Vip, ifacePri, OutFile):

	OutputFile = open(OutFile,"w")
	
	for port in ports:
		
		tempPort = randomPort()
		#Sending the SYN packet and saving the return packet
		maybeSYNACKpkt = sr1(IP(dst = Vip)/TCP(sport = tempPort, dport = port, flags = "S"), iface = ifacePri, timeout = 3) #depending on game setup, we may just delete the iface argument. sr1 will use the default iface. We may also want to update the timeout value
		
		if maybeSYNACKpkt:
			OutputFile.write( str(maybeSYNACKpkt.getlayer(TCP).flags) + " " + str(port) + "\n")
			checkflags = maybeSYNACKpkt.getlayer(TCP).flags
			if checkflags == 'SA': #We are hoping to see a SynAck flag here
				print
				OutputFile.write("Port {} is Open \n".format(port))#this is really just a placeholder. We will probably want to feed this output file to another program (such as a port to service matcher)
				print("Port {} is Open \n".format(port))
			else:	
				print("Port {} is Closed \n".format(port))
		
			#eitherway, send a reset packet. Using send so it doesn't wait for a reply
			ResetPkt = send(IP(dst = Vip)/TCP(sport = tempPort, dport = port, flags = "R"), iface = ifacePri) # we want to send the Reset packet, so that the scan (hopefully) goes undetected
		else:
			print ("Host did not respond!! \n") # special case where the host did not respond. May be down, or just programmed to not respond to TCP connections at all.
	
	OutputFile.close()



# type determines the type of the argument
def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--interface', dest='iface', required=True, help="Interface to listen on")
	parser.add_argument('--victim-ip', dest='Vip', required=True, help="Victim Ip Address")
	parser.add_argument('--min-port', dest='MinP', required=True, help="Lowest Port to be Scanned")
	parser.add_argument('--max-port', dest='MaxP', required=True, help="Highest Port to be Scanned")
	parser.add_argument('--outfile', dest='OutFile', required=True, help="Output File")
	parser.add_argument('--scantype', dest= 'scantype', required=True, help="Current scan options are SYNscan, <as more options are added, list them here>")
	#right now, there is no error checking. Put it on the To Do list.
	args = parser.parse_args()
	ifacePri = args.iface
	Vip = args.Vip #if you want to test it 45.33.32.156 is scanme.nmap.org, a free scannable server that gives you full permissions to scan (visit in browser for the readme)

	MinP = args.MinP
	MaxP = args.MaxP
	OutFile = args.OutFile
	ports = range(int(MinP), int(MaxP)+1)
	if args.scantype == "SYNscan":
		SYNScan(ports, Vip, ifacePri, OutFile)
	
	#add more scan types here
	
	else:
		print("Not a valid scan type. Goodbye")

	
if __name__ == '__main__':
	main()
