#!/usr/bin/env python3

import subprocess
import sys, getopt, os
import threading
import argparse

cwd = os.getcwd()
path = cwd + "/port_scanner_files/"
ip_list_file = path + "input/IP_list.txt"
nmap_output_file = path + "temp_output/nmap_output"
#the scorchedearth option runs every nmap scan that doesn't require an additional host OR standard ping scan
scorchedearth = ["-sS", "-sT", "-sA", "-sW", "-sM", "-sU", "-sN", "-sF", "-sX", "-sY","-sZ", "-sO"]

def module_name():
  return "quiet-scan-threaded"

def module_help():
  return "quiet port scanner tool (threaded)"

def module_usage():
  return "{0}".format(module_name())

def system_call(program_name, args = [], privilege = False):

    call = program_name
    
    if(privilege == True):
        call = "sudo " + call

    for arg in args:
        call = call + " " + arg

    print(call)

    subprocess.call(call, shell=True)


def parse_nmap_output(ipAddr, scantype, nmap_output):
    services_list = path + "scan_output/services_list" + "_" + ipAddr + ".txt"
    nmap_fp = open(nmap_output, 'r')

    line_in = nmap_fp.readline()

    while(line_in.find("STATE") == -1 and line_in.find("SERVICE") == -1): #Fixed a bug in this line as it was looping infinitely because the previous check was "STATE SERVICE", but sometimes, we endup in getting an extra space and none of the lines match
        line_in = nmap_fp.readline()
        if(line_in.lower().find("nmap done") != -1): #when no ports are open we should exit
            return
    #changed to append, so we can get results from all scan types
    services_fp = open(services_list, 'a')

    line_in = nmap_fp.readline()
            
    while (line_in and line_in.strip() != ''):
        if(line_in.lower().find("closed") != -1): #IF port is closed, continue parsing the next line
            line_in = nmap_fp.readline()
            continue

        str_split = line_in.split('/')
        str_split_2 = str_split[-1].split(' ')

        line_out_list = []

        line_out_list.append(str_split[0])
        line_out_list.extend(str_split_2)

        line_out = ' '.join(line_out_list)
        services_fp.write("Scanned with: " + scantype + "\n")#write what scan produced these results
        services_fp.write(line_out)

        line_in = nmap_fp.readline()
            
    services_fp.close()
    nmap_fp.close()


def buildArgs(argv, line, fileName):
    arr = [line.strip()]
    if(len(argv) > 0):
        arr.extend(argv)
    arr.append("-Pn") #controversial addition: we know all the hosts are going to be online because of the game rules, so adding this skips the host discovery
    arr.extend([">", fileName])
    return arr      

def nmap_worker(line, scantype, standard_args):

    #since we are appending multiple scan results to one file, zero out the file before start
    line = line.strip()
    services_list = path + "scan_output/services_list" + "_" + line + ".txt"
    services_fp = open(services_list, 'w')
    services_fp.close()
    
    if ("scortchedearth" in scantype) or ("se" in scantype):
    	scantype = scorchedearth
    for scan in scantype:
    	
    	print("Starting NMAP Thread for " + line +":" + " Scantype: " + scan)
    	fileName = nmap_output_file + "_" + line + ".txt"
    	system_call(("nmap " + scan), buildArgs(standard_args, line, fileName), True) #-p- to scan all the ports
    	parse_nmap_output(line, scan, fileName)



def main():  
    with open(ip_list_file ,'r') as file:
        line = file.readline()
        
        #New calling convention is two lists of arguments: the scan type and whatever other arguments there are
        #example python3 quiet-scan-threaded.py --scantype "-sS -sN" --options "-p 80 -sV"

        parser = argparse.ArgumentParser()
        parser.add_argument('--scantype', dest= 'scantype', required=True, help="List all scan types here. Format as if callingi n nmap ie -sS -Su -sM' etc. To automatically run all scan types enter 'scortchedearth' or 'se'")
        parser.add_argument('--options', dest= 'standard_args', nargs='+', required=True, help="All options other than scan type listed here, just as if calling nmap from the commandline")
        args = parser.parse_args()
        standard_args = args.standard_args
        scans = args.scantype
        scantype = scans.split(' ')

       	
        while line:
            t = threading.Thread(target=nmap_worker, args=(line, scantype, standard_args))
            t.start()
            line = file.readline() 

if __name__ == "__main__":
  main()
