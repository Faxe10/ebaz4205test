import csv
import time
import logging
import sys, os
from fileinput import filename

from pyvisa_py.common import LOGGER

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
    runs = 25
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
    url = "http://10.140.1.238:8082/api/get_data" + str(data_port)
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
    time_start_seq = datetime.datetime.now()
    afg.set_offset(2, 0)
    filename = next_free_filename("sequenz1_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for  i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1,v_current)
            v_current += v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1] # have error in api, don't want to connect to api server
            data3_pins_state = request_data(3)[1]
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
            #save_csv(filename,data,v_current )
        msg = "Finished Sequenz 1 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)
    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 1 finished in: " + str(time_passed)
    logging.info(log_msg)

def sequenz2(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    filename = next_free_filename("sequenz2_run")
    afg.set_offset(1, 0)
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(1)[3]
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 2 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 2 finished in: " + str(time_passed)
    logging.info(log_msg)
def sequenz3(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(2, 3.2)
    afg.set_offset(1, 0)
    filename = next_free_filename("sequenz3_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename, data, v_current)
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 3 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)
    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 3 finished in: " + str(time_passed)
    logger.info(log_msg)
def sequenz4(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(1, 3.2)
    filename = next_free_filename("sequenz4_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename, data, v_current)
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 4 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 4 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz5(v_start, v_end, v_step,wait_time,afg,runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(2, 0)
    filename = next_free_filename("sequenz5_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1,v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename,data,v_current )
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 5 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 5 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz6(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(1, 0)
    filename = next_free_filename("sequenz6_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename, data, v_current)
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 6 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 6 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz7(v_start, v_end, v_step,wait_time,afg,runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(2, 3.2)
    filename = next_free_filename("sequenz7_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1,v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename,data,v_current )
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 7 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 7 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz8(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    afg.set_offset(1, 3.2)
    filename = next_free_filename("sequenz8_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename, data, v_curren0t)
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 8 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 8 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz9(v_start, v_end, v_step,wait_time,afg,runs):
    time_start_seq = datetime.datetime.now()
    filename = next_free_filename("sequenz9_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        new_csv(filename)
        v_current = v_start
        while v_current < v_end:
            afg.set_offset(1,v_current)
            afg.set_offset(2, v_current)
            v_current += v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename,data,v_current )
            try:
                data[measurment_counter].append(data_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1
        msg = "Finished Sequenz 9 run:" + str(run_counter)
        logger.info(msg)
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 9 finished in: " + str(time_passed)
    logger.info(log_msg)

def sequenz10(v_start, v_end, v_step, wait_time, afg, runs):
    time_start_seq = datetime.datetime.now()
    filename = next_free_filename("sequenz10_run")
    new_csv(filename)
    run_counter = 1
    data = []
    data.append(["Voltage"])
    for i in range(runs):
        measurment_counter = 1
        run = "run" + str(run_counter)
        run_counter = run_counter + 1
        data[0].append(run)
        new_csv(filename)
        v_current = v_start
        while v_current > v_end:
            afg.set_offset(1, v_current)
            afg.set_offset(2, v_current)
            v_current -= v_step
            time.sleep(wait_time)
            data1_pins_state = request_data(1)[1]
            data3_pins_state = request_data(3)[1]
            #save_csv(filename, data, v_current)
            try:
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            except:
                data.append([v_current])
                data[measurment_counter].append(data1_pins_state)
                data[measurment_counter].append(data3_pins_state)
            measurment_counter = measurment_counter + 1

        msg = "Finished Sequenz 10 run:" + str(run_counter)
        logger.info(msg)

    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        for row in data:
            wr.writerow(row)

    time_passed = datetime.datetime.now() - time_start_seq
    time_now = datetime.datetime.now()
    log_msg = str(time_now) + "  Sequenz 10 finished in: " + str(time_passed)
    logger.info(log_msg)

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
        "data1": 0,
        "data2": 0,
    }
    df = pd.DataFrame([row])
    df.to_csv(filename,mode="a",header=True,index=False)
if __name__ == '__main__':
    main()