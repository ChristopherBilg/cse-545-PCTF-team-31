#!/usr/bin/env python3

import swpag_client

URL = "<INSERT DURING CTF AND COMMIT>"
TEAM_URL = "http://" + URL + "/"
TEAM_FLAG_TOKEN = "<INSERT DURING CTF AND COMMIT>"

def module_name():
  return "target-info"

def module_help():
  return "find relevant information about the CTF event target machines (make sure to ignore our own)"

def module_usage():
  return "{0}".format(module_name())

def main():
  try:
    team = swpag_client.Team(TEAM_URL, TEAM_FLAG_TOKEN)
    target_info = team.get_targets()

    for target in target_info:
        print(target['team_name'])
        print(target['hostname'])
        print(target['port'])
        print(target['flag_id'])
        
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()
