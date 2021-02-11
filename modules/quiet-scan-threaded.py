#!/usr/bin/env python3

import subprocess
import sys, getopt, os
import threading

cwd = os.getcwd()
path = cwd + "/modules/port_scanner_files/"
ip_list_file = path + "input/IP_list.txt"
nmap_output_file = path + "temp_output/nmap_output"

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


def parse_nmap_output(ipAddr, nmap_output):
    services_list = path + "scan_output/services_list" + "_" + ipAddr + ".txt"
    nmap_fp = open(nmap_output, 'r')

    line_in = nmap_fp.readline()

    while(line_in.find("STATE") == -1 and line_in.find("SERVICE") == -1): #Fixed a bug in this line as it was looping infinitely because the previous check was "STATE SERVICE", but sometimes, we endup in getting an extra space and none of the lines match
        line_in = nmap_fp.readline()
        if(line_in.lower().find("nmap done") != -1): #when no ports are open we should exit
            return

    services_fp = open(services_list, 'w')

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
        
        services_fp.write(line_out)

        line_in = nmap_fp.readline()
            
    services_fp.close()
    nmap_fp.close()


def buildArgs(argv, line, fileName):
    arr = [line.strip()]
    if(len(argv) > 0):
        arr.extend(argv)
    arr.extend([">", fileName])
    return arr      

def nmap_worker(line, argv):
    line = line.strip()
    print("Starting NMAP Thread for " + line + ":")
    fileName = nmap_output_file + "_" + line + ".txt"
    system_call("nmap -sS", buildArgs(argv, line, fileName), True) #-p- to scan all the ports
    parse_nmap_output(line, fileName)



def main(argv):  
    with open(ip_list_file ,'r') as file:
        line = file.readline()
        while line:
            t = threading.Thread(target=nmap_worker, args=(line, argv))
            t.start()
            line = file.readline()

if __name__ == "__main__":
  main(sys.argv[1:])
