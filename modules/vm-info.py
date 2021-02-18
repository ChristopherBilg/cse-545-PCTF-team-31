#!/usr/bin/env python

import swpag_client

URL = "<INSERT DURING CTF AND COMMIT>"
TEAM_URL = "http://" + URL + "/"
TEAM_FLAG_TOKEN = "<INSERT DURING CTF AND COMMIT>"

def module_name():
  return "vm-info"

def module_help():
  return "find relevant information about the CTF event virtual machine (VM)"

def module_usage():
  return "{0}".format(module_name())

def main():
  try:
    team = swpag_client.Team(TEAM_URL, TEAM_FLAG_TOKEN)
    vm_info = team.get_vm()

    for key, value, in vm_info.items():
        print("{0}: {1}".format(key, value))
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
