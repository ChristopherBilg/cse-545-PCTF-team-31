#!/usr/bin/env python3

import subprocess
import sys

def module_name():
  return "service-backup"

def module_help():
  return "initial module to run to backup all service files"

def module_usage():
  return "{0} <destination_directory>".format(module_name())

def format_arguments():
  if len(sys.argv) < 2:
    print(module_usage())
    sys.exit(1)

  return {
    "destination_directory": sys.argv[1],
  }

def main():
  args = format_arguments()
  destination_directory = args["destination_directory"]

  try:
    subprocess.Popen("cp -rf /opt {0}".format(destination_directory), shell=True)
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
