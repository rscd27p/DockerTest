#!/usr/bin/python

import hightime
import time
import sys
#import rpyc
import nidcpower

'''
connection = rpyc.connect('midoe1', 18861)
nidcpower = connection.root.nidcpower
nidmm = connection.root.nidmm
'''

def route_meas():
	# Simulated Flag
	SIMULATE = False
	print('Starting the program ...')
	my_smu = nidcpower.Session(resource_name='PXI1Slot2', channels='0')
	my_smu.source_mode.SINGLE_POINT
	my_smu.output_function = nidcpower.OutputFunction.DC_VOLTAGE
	my_smu.voltage_level = 2.5
	my_smu.current_limit = 0.05
	my_smu.voltage_level_autorange = True
	my_smu.current_limit_autorange = True
	my_smu.source_delay = hightime.timedelta(seconds=0.1)
	

	#Start voltage generation in CH0
	print('Setting Power Supply CH0 to 2.5V ...')
	my_smu.initiate()
	my_smu.wait_for_event(nidcpower.Event.SOURCE_COMPLETE)

	my_smu.export_attribute_configuration_file('/home/nitest/Documents/DockerTest/smu_config.nidcpowerconfig')
route_meas()


