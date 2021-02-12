#!/usr/bin/env python3

import math
import subprocess
import time

SLEEP_TIME = 2 * 60

def module_name():
  return "auto-runner"

def module_help():
  return "automatically run scripts/modules/executables/etc. every X seconds"

def module_usage():
  return "{0}".format(module_name())

def main():
  start_time = time.time()
  
  try:
    with open("./auto-runner.txt", "r") as runner_commands:
      command = runner_commands.readline()
      count = 1
      while command:
        print("{0}. Running: {1}".format(count, command[:-1]))
        
        subprocess.Popen(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        
        count = count + 1
        command = runner_commands.readline()
  except Exception as e:
    print(e)

  end_time = time.time()
  total_time = math.ceil(end_time - start_time)
  sleep_time = SLEEP_TIME - total_time

  print("\nAuto-runner command execution took {0} seconds, sleeping for {1} seconds before running again.\n".format(total_time, sleep_time))
  time.sleep(sleep_time)

  main()
      


if __name__ == "__main__":
  main()
