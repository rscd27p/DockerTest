#!/usr/bin/python

import argparse
import rpyc
import time

HOSTNAME = 'dmmts-dut'
PORT = 18861

connection = rpyc.connect(HOSTNAME, PORT)
nidmm = connection.root.nidmm

parser = argparse.ArgumentParser(description='Performs a waveform acquisition using the NI-DMM API.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-n', '--name', default='PXI1Slot2', help='Resource name of a National Instruments Digital Multimeter.')
# this dir(nidmm.Function) thing is a dirty dirty hack and I just used it because I was having issues with nidmm.Function.__members__.keys(), I thought it was a problem with using python 2.7, but I've seen it with 3.6 as well
# https://stackoverflow.com/questions/44446945/python-how-to-get-name-of-the-enum
parser.add_argument('-f', '--function', default='WAVEFORM_VOLTAGE', choices=dir(nidmm.Function), type=str.upper, help='Measurement function.')
parser.add_argument('-r', '--range', default=10, type=float, help='Measurement range.')
parser.add_argument('-d', '--digits', default=6.5, type=float, help='Digits of resolution for the measurement.')
parser.add_argument('-p', '--points', default=10, type=int, help='Specifies the number of points to acquire before the waveform acquisition completes.')
parser.add_argument('-s', '--rate', default=1000, type=int, help='Specifies the rate of the acquisition in samples per second.')
args = parser.parse_args()


with nidmm.Session(args.name) as session:
    session.configure_waveform_acquisition(nidmm.Function[args.function], args.range, args.rate, args.points)
    with session.initiate():
        while True:
            time.sleep(0.1)
            backlog, acquisition_state = session.read_status()
            if (acquisition_state == nidmm.AcquisitionStatus.FINISHED_WITH_NO_BACKLOG):
                break
            measurements, samples_acquired = session.fetch_waveform(array_size=backlog)
            print(measurements)