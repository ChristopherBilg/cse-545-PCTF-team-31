#!/usr/bin/env python3

import sys

def module_name():
  return "example"

def module_help():
  return "an example module for the script runner"

def module_usage():
  return "{0} <arg1> [arg2 arg3]".format(module_name())

def main():
  print("Hello world!")
  print("Example output:", " ".join(sys.argv))

if __name__ == "__main__":
  main()
