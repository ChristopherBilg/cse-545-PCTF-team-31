#!/usr/bin/env python3

import pyshark
import sys

def module_name():
  return "nta"

def module_help():
  return """network traffic analyzer tool
    Green: Source IP is this machine
    Red  : Source IP is a different machine"""

def module_usage():
  return "{0} <interface> <interface_inet>".format(module_name())

def format_arguments():
  if len(sys.argv) < 3:
    print(module_usage())
    sys.exit(1)

  return {
    "interface": sys.argv[1],
    "interface_inet": sys.argv[2]
  }

def main():
  args = format_arguments()

  interface = args["interface"]
  interface_inet = args["interface_inet"]
  
  try:
    capture = pyshark.LiveCapture(interface=interface)
    print("Waiting for packets to sniff...")

    for packet in capture.sniff_continuously():
      if not "ip" in packet:
        continue

      if (packet["ip"].src == interface_inet):
        print("\033[0;32m", packet, "\033[0m")
      else:
        print("\033[0;31m", packet, "\033[0m")

      input("Press enter to display the next sniffed packet...")
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
