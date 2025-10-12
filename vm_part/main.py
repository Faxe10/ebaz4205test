import csv
import time
import logging
import sys, os
from fileinput import filename

sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Projekt-Root
import requests
import numpy as np
import datetime
import pandas as pd
from tektronixAFG31252 import AFG31252

logger = logging.getLogger(__name__)
def main():
    time_now = str(datetime.date.today())
    log_filename = 'measurments' + time_now + '.log'
    logging.basicConfig(filename=log_filename,level=logging.INFO)
    logger.info('start_setup')
    afg_ip = '10.140.1.17'
    afg = AFG31252(afg_ip)
    afg.set_waveform(1, "DC")
    afg.set_waveform(2, "DC")
    afg.set_high_limit(1, 3.3)
    afg.set_high_limit(2, 3.3)
    afg.set_low_limit(1, 0)
    afg.set_low_limit(2, 0)
    v_start = 0
    v_end = 3.201
    v_step = 0.001
    wait_time = 0.1 #time wait befor check in s
def request_data(data_port):
    url = "http://10.140.1.124:8082/api/get_data" + str(data_port)
    response = requests.get(url)
    return response.json()

def sequenz1(v_start, v_end, v_step,wait_time,afg):
    v_current = v_start
    filename = "sequenz1.csv"
    new_csv(filename)
    while v_current < v_end:
        afg.set_offset(1,v_current)
        v_current += v_step
        time.sleep(wait_time)
        data = request_data(1)
        save_csv(filename,data,v_current )


def save_csv(filename, data,v_current):
    row = {
        "voltage":v_current,
        "data": data,
    }
    df = pd.DataFrame([row])
    df.to_csv(filename,mode="a",header=False,index=False)

def new_csv(filename):
    row = {
        "voltage": 0,
        "data": 0,
    }
    df = pd.DataFrame([row])
    df.to_csv(filename,mode="a",header=True,index=False)