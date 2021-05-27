#!/usr/bin/python

import hightime
import nidcpower
import niswitch
import nidmm
import time
import sys

def route_meas():
	# Simulated Flag
	SIMULATE = False
	print('Starting the program ...')
	with nidcpower.Session(resource_name='PXI1Slot2', channels='0') as dc_power:
	print('Setting Power Supply CH0 to 5V ...')
	dc_power.initiate()
	dc_power.wait_for_event(nidcpower.Event.SOURCE_COMPLETE, hightime.timedelta(seconds=10))

	with niswitch.Session(resource_name="PXI1Slot7") as sw_switch:
		start = time.perf_counter()
		print('Test1')
		sw_session.connect(channel1= 'ch0', channel2= 'com')
		end = time.perf_counter()
		print('Channel CH0 and COM0 are now connected. Task completed in', str(end-start),'seconds')
	
	#DMM Session
	start = time.perf_counter()
	dmm_session = nidmm.Session("PXI1Slot4")
	dmm_session.configureMeasurementDigits(nidmm.Function.DC_VOLTS, 10, 5.5)
	end = time.perf_counter()
	print("Measurement: " + str(dmm_session.read()), 'Task completed in', str(end-start),'seconds')
	start = time.perf_counter()
	sw_session.disconnect(channel1= 'ch0', channel2= 'com')
	end = time.perf_counter()
	print('Channel CH0 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')
	time.sleep(3)
	print('Routing AI to GND ...')
	start = time.perf_counter()
	sw_session.connect(channel1= 'ch1', channel2= 'com')
	end = time.perf_counter()
	print('Channel CH1 and COM0 are now connected. Task completed in', str(end-start),'seconds')
	#AI Read
	start = time.perf_counter()
	dmm_session.configureMeasurementDigits(nidmm.Function.DC_VOLTS, 10, 5.5)
	end = time.perf_counter()
	print("Measurement: " + str(dmm_session.read()), 'Task completed in', str(end-start),'seconds')
	start = time.perf_counter()
	sw_session.disconnect(channel1= 'ch1', channel2= 'com')
	end = time.perf_counter()
	print('Channel CH1 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')
	print('Ending the program ...')
	#Close DC Power Session
	dc_session.reset()
	
start = time.perf_counter()
route_meas()
end = time.perf_counter()
print('Completed execution in', str(end-start),'seconds')
