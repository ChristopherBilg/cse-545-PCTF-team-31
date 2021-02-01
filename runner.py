#!/usr/bin/env python3

import argparse
import glob
import importlib
import os
import pathlib

def module_list():
  print("\nModules:")

  for potential_module in glob.glob("./modules/*.py"):
    try:
      module_name = "modules.{0}".format(pathlib.Path(potential_module).stem)
      imported_module = importlib.import_module(module_name)

      print("")
      print("  {0}:".format(imported_module.module_name()))
      print("    \"{0}\"".format(imported_module.module_help()))
      print("    Usage: {0}".format(imported_module.module_usage()))
    except:
      pass

def main(args):
  if args.module is not None:
    os.system("python3 ./modules/{0}.py {1}".format(args.module[0], " ".join(args.args)))
    return

  module_list()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="ASU CSE 545 - Team 31 - CTF Project")
  parser.add_argument("-m", "--module", help="the module to run", dest="module", metavar="module", nargs=1)
  parser.add_argument("-a", "--args", "--arguments", help="the arguments to run with the module", dest="args", metavar="args", nargs="*", default=[])
  parser.add_argument("-l", "--list", help="list all of the available modules to run", dest="list", action="store_true")
  args = parser.parse_args()

  main(args)
