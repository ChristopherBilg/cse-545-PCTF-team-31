#!/usr/bin/env python3

import swpag_client

TEAM_URL = "http://127.0.0.1/"
TEAM_FLAG_TOKEN = "<INSERT DURING CTF AND COMMIT>"

def module_name():
  return "flag-submitter"

def module_help():
  return "submit all flags in the \"./flag-submitter.txt\" file"

def module_usage():
  return "{0}".format(module_name())

def main():
  try:
    with open("./flag-submitter.txt", "r") as flags_file:
      all_flags = flags_file.read().splitlines()
      team = swpag_client.Team(TEAM_URL, TEAM_FLAG_TOKEN)

      print(all_flags)
      success = team.submit_flag(all_flags)
      print(success)
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
