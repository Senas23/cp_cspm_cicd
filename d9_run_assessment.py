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

def run_assessment(bundle_id, aws_cloud_account, d9_secret, d9_key, maxTimeoutMinutes=10):
    global t0,total_sec
    t0_run_assessment = datetime.datetime.utcnow()
    t0 = datetime.datetime.utcnow()
    print(f"\n Dome9 Run Assessment Interface Version - {APIVersion}")
    print(f"{star_divider}Starting Assessment Execution{star_divider}")

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    body = {
        "id": bundle_id,
        "cloudAccountId": aws_cloud_account,
        "cloudAccountType": "Aws"
    }

    r = requests.post(f'{D9_URL}/assessment/bundleV2', data=json.dumps(body), headers=headers, auth=(d9_key, d9_secret))
    r.raise_for_status()
    tn = datetime.datetime.utcnow()

    #check that max timeout was not reached
    if checkThatMaxTimeWasNotReached(t0, maxTimeoutMinutes):
        return

    total_sec = total_sec + (tn - t0).total_seconds()

    print(f"{star_divider}Assessment Execution Done in {(tn - t0_run_assessment).total_seconds()} seconds{star_divider}")

    return r.json()

def checkThatMaxTimeWasNotReached (t0, maxTimeoutMinutes):
    tNow = datetime.datetime.utcnow()
    elapsed = (tNow - t0).total_seconds()
    print(f'\nCurrent run time of d9 assessment execution and analyzing is - {elapsed} Seconds\n')
    if elapsed > maxTimeoutMinutes * 60:
        print(f'\nStopping script, passed maxTimeoutMinutes ({maxTimeoutMinutes})')
        return True
    return False

def main():
  global star_divider
  star_divider = Divider()
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--awsAccountNumber', required=True, type=str)
  parser.add_argument('--bundleId', required=True, type=int)
  parser.add_argument('--maxTimeoutMinutes', required=False, type=int, default=10)
  args = parser.parse_args()
  # Take start time
  print("\n\n{}\nStarting...\n{}\n\nSetting now (UTC {}) ".format(80 * '*', 80 * '*', t0))
  result = run_assessment(bundle_id=args.bundleId, aws_cloud_account=args.awsAccountNumber, 
                          d9_key=os.environ.get('DOME9_ACCESS_ID'), d9_secret=os.environ.get('DOME9_SECRET_KEY'), 
                          maxTimeoutMinutes=args.maxTimeoutMinutes)
  return

if __name__ == "__main__":
  main()
