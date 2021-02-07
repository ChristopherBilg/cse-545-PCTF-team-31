#!/usr/bin/env python3

import subprocess

path = "/mnt/hgfs/CSE545/PCTF/"
ip_list_file_name = "IP_list.txt"
ip_list_file = path + ip_list_file_name
nmap_output_file = "nmap_output.txt"

def module_name():
  return "quiet-scan"

def module_help():
  return "quiet port scanner tool"

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


def parse_nmap_output(nmap_output = "nmap_output.txt", services_list = "services_list.txt"):

    nmap_fp = open(nmap_output, 'r')

    line_in = nmap_fp.readline()

    while(line_in.find("STATE SERVICE") == -1):
        line_in = nmap_fp.readline()

    services_fp = open(services_list, 'w')

    line_in = nmap_fp.readline()
            
    while (line_in and line_in.strip() != ''):
        
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


def main():
  
    with open(ip_list_file ,'r') as file:

        line = file.readline()
        
        while line:
            system_call("nmap -sS", [line.strip(), ">", nmap_output_file], True)
            line = file.readline()

    parse_nmap_output(nmap_output_file)

if __name__ == "__main__":
  main()
