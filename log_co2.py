import mh_z19 as m19
import argparse
from datetime import datetime, timedelta
from typing import Dict
import time

def parse_args() -> Dict:
  parser = argparse.ArgumentParser(
        prog="log_c02",
        description="Log CO2 concentration at given interval for given time period."
        )
  parser.add_argument("-p", "--ping_interval", type=int, help="Number of seconds between sensor reads.", default=30)
  parser.add_argument("-t0", "--start_datetime", type=lambda date_str: datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f"), help="Date in YYYY-MM-DDTHH:MM:SS.ffffff format. Defaults to current time.", default=datetime.now())
  parser.add_argument("-t1", "--end_datetime", type=lambda date_str: datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f"), help="Date in YYYY-MM-DDTHH:MM:SS.ffffff format. Defaults to one hour from current time.", default=datetime.now() + timedelta(hours=1))
  parser.add_argument("-l", "--log_file_path", type=str, help="Full path to output logfile.", default="co2-log.txt")

  args = parser.parse_args()
  args = vars(args)
    
  return args


def append_data_to_file(file_name: str, datum: str) -> None:
  with open(file_name, "a") as f:
    f.write(",".join([datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), str(datum)]))
    f.write("\n")

        
if __name__ == "__main__":
  args = parse_args()
  while args["start_datetime"] < datetime.now() < args["end_datetime"]:
    co2_datum = m19.read()
    append_data_to_file(args["log_file_path"], co2_datum["co2"])
    time.sleep(args["ping_interval"])
