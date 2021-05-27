#!/usr/bin/python

import hightime
import time
import sys
import rpyc

connection = rpyc.connect('midoe1', 18861)
nidcpower = connection.root.nidcpower
nidmm = connection.root.nidmm

def route_meas():
	# Simulated Flag
	SIMULATE = False
	print('Starting the program ...')
	my_smu = nidcpower.Session(resource_name='PXI1Slot2', channels='0')
	my_dmm = nidmm.Session("PXI1Slot4")
	#Configure DC Power Output
	#nidcpower.Session.source_mode.SINGLE_POINT
	#my_smu.output_function = nidcpower.OutputFunction.DC_VOLTAGE
	#print(dir(my_smu))
	#my_smu.voltage_level = 2.5
	#my_smu.voltage_level = 2.5
	#my_smu.current_limit = 0.05
	#my_smu.voltage_level_autorange = True
	#my_smu.current_limit_autorange = True
	#my_smu.source_delay = hightime.timedelta(seconds=0.1)

	#Start voltage generation in CH0
	print('Setting Power Supply CH0 to 2.5V ...')
	my_smu.initiate()
	my_smu.wait_for_event(nidcpower.Event.SOURCE_COMPLETE)
	time.sleep(5)
	my_dmm.configure_measurement_digits(nidmm.Function.DC_VOLTS, 10, 7.5)
	print("Measurement: " + str(my_dmm.read()))

	my_smu.reset()
	return 0

def display_rlts(route_a, route_b, nroute_a, nroute_b, meas_1, meas_2, total_ex):
	print('')
	print('******************************************************')
	print('*                  Timing Results                    *')
	print('******************************************************')
	print('Task                         * Time (ms)              ')
	print('******************************************************')
	print('Connect CHO to COM           *', str(route_a))
	print('Take DMM Measurement 1       *', str(meas_1))
	print('Disconnect CH0 and COM       *', str(nroute_a))
	print('Connect CH1 to COM           *', str(route_b))
	print('Take DMM Measurement 2       *', str(meas_2))
	print('Disconnect CH0 and COM       *', str(nroute_b))
	print('Total Execution Time         *', str(total_ex))
	print('******************************************************')


route_meas()


