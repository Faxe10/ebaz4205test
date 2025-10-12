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
from pathlib import Path

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
    wait_time = 0.01 #time wait befor check in s
    runs = 1
    sequenz1(v_start,v_end,v_step,wait_time,afg, runs)
    sequenz2(v_start, v_end, v_step, wait_time, afg, runs)
    sequenz3(v_start, v_end, v_step, wait_time, afg, runs)
    sequenz4(v_start, v_end, v_step, wait_time, afg, runs)
    sequenz5(v_end, v_start, v_step, wait_time, afg, runs)
    sequenz6(v_end, v_start, v_step, wait_time, afg, runs)
    sequenz7(v_end, v_start, v_step, wait_time, afg, runs)
    sequenz8(v_end, v_start, v_step, wait_time, afg, runs)
    sequenz9(v_start, v_end, v_step, wait_time, afg, runs)
    sequenz10(v_end, v_start, v_step, wait_time, afg, runs)

def request_data(data_port):
    url = "http://10.140.1.155:8082/api/get_data" + str(data_port)
    response = requests.get(url)
    print(response)
    return response.json()

def next_free_filename(base_name, ext=".csv"):
    n = 1
    while True:
        filename = f"{base_name}{n}{ext}"
        if not Path(filename).exists():
            return filename
        n += 1
def sequenz1(v_start, v_end, v_step,wait_time,afg,runs):
    filename = next_free_filename("sequenz1_run")
    new_csv(filename)
    afg.set_offset(2, 0)
    for  i in range(runs):
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1,v_current)
            v_current += v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename,data,v_current )


def sequenz2(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz2_run")
    new_csv(filename)
    afg.set_offset(1, 0)
    for i in range(runs):
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)

def sequenz3(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz3_run")
    new_csv(filename)
    afg.set_offset(2, 3.2)
    for i in range(runs):
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)

def sequenz4(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz4_run")
    new_csv(filename)
    afg.set_offset(1, 3.2)
    for i in range(runs):
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)


def sequenz5(v_start, v_end, v_step,wait_time,afg,runs):
    filename = next_free_filename("sequenz5_run")
    new_csv(filename)
    afg.set_offset(2, 0)
    for  i in range(runs):
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1,v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename,data,v_current )


def sequenz6(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz6_run")
    new_csv(filename)
    afg.set_offset(1, 0)
    for i in range(runs):
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)

def sequenz7(v_start, v_end, v_step,wait_time,afg,runs):
    filename = next_free_filename("sequenz7_run")
    new_csv(filename)
    afg.set_offset(2, 3.2)
    for  i in range(runs):
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1,v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename,data,v_current )


def sequenz8(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz8_run")
    new_csv(filename)
    afg.set_offset(1, 3.2)
    for i in range(runs):
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)

def sequenz9(v_start, v_end, v_step,wait_time,afg,runs):
    filename = next_free_filename("sequenz9_run")
    new_csv(filename)
    for  i in range(runs):
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1,v_current)
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename,data,v_current )

def sequenz10(v_start, v_end, v_step, wait_time, afg, runs):
    filename = next_free_filename("sequenz10_run")
    new_csv(filename)
    for i in range(runs):
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1, v_current)
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data = request_data(1)
            save_csv(filename, data, v_current)

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
if __name__ == '__main__':
    main()