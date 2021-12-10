# 3rd party libraries
import requests  # $ pip3 install requests

# python standard libraries
import json
import argparse
import datetime
import os
from dataclasses import dataclass # $ pip3 install dataclasses

t0 = datetime.datetime.utcnow()
total_sec = 0
APIVersion=0.01
D9_URL = 'https://api.dome9.com/v2'

@dataclass
class Divider:
    length: int = 50
    divider_char: str = "*"
    prefix: str = "\n"
    suffix: str = "\n"
    def __str__(self):
        return self.prefix + (self.divider_char * self.length) + self.suffix

def update_rule_bundle(bundle_id, d9_secret, d9_key, maxTimeoutMinutes=10):

    global t0,total_sec
    t0_run_assessment = datetime.datetime.utcnow()
    t0 = datetime.datetime.utcnow()
    print("\n CSPM Update Bundle Interface Version - {}".format(APIVersion))
    print(f"{star_divider_50}Starting Update Bundle Execution{star_divider_50}")

    with open(f'rules/{bundle_id}.json') as jsonFile:
      rules = json.load(jsonFile)

    body = {
      "id": bundle_id,
      "name": "Art - [Deprecated] AWS CloudGuard Network Alerts",
      "description": "This ruleset is deprecated. Please move to the AWS CloudGuard Network Alerts for default VPC components ruleset",
      "rules": rules,
      "cloudVendor": "aws"
    }

    r = requests.put(f'{D9_URL}/Compliance/Ruleset/{bundle_id}', json=body,
                      auth=(d9_key, d9_secret))
    r.raise_for_status()
    tn = datetime.datetime.utcnow()

    #check that max timeout was not reached
    if checkThatMaxTimeWasNotReached(t0, maxTimeoutMinutes):
        return

    total_sec = total_sec + (tn - t0).total_seconds()

    print(f"{star_divider_50}Update Bundle Execution Done in {(tn - t0_run_assessment).total_seconds()} seconds{star_divider_50}")

    return r.json()

def checkThatMaxTimeWasNotReached (t0, maxTimeoutMinutes):
    tNow = datetime.datetime.utcnow()
    elapsed = (tNow - t0).total_seconds()
    print('\nCurrent run time of D9 Update Bundle execution is - {} Seconds\n'.format(elapsed))
    if elapsed > maxTimeoutMinutes * 60:
        print('\nStopping script, passed maxTimeoutMinutes ({})'.format(maxTimeoutMinutes))
        return True
    return False

def main():
  global star_divider_50, star_devider_80
  star_divider_50 = Divider()
  star_divider_80 = Divider(length=80)
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--bundleId', required=True, type=int)
  parser.add_argument('--maxTimeoutMinutes', required=False, type=int, default=10)
  args = parser.parse_args()
  # Take start time
  print(f"\n{star_divider_80}Starting...{star_divider_80}\nSetting now (UTC {t0}) ")
  result = update_rule_bundle(bundle_id=args.bundleId, 
                              d9_key=os.environ.get('DOME9_ACCESS_ID'),
                              d9_secret=os.environ.get('DOME9_SECRET_KEY'),
                              maxTimeoutMinutes=args.maxTimeoutMinutes)
  return

if __name__ == "__main__":
  main()
