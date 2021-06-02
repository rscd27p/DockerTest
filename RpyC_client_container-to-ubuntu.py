#!/usr/bin/python

import hightime
import time
import sys
import rpyc

connection = rpyc.connect('midoe1', 18861, config={'allow_public_attrs': True,  'allow_all_attrs': True})
niswitch = connection.root.niswitch
nidcpower = connection.root.nidcpower
nidmm = connection.root.nidmm

def route_meas():
	# Simulated Flag
	SIMULATE = False
	print('Starting the program ...')
	with nidmm.Session("PXI1Slot4") as my_dmm:
		with nidcpower.Session(resource_name='PXI1Slot2', channels='0') as my_smu:
			with niswitch.Session(resource_name="PXI1Slot7", topology= '2575/2-wire 95x1 Mux', reset_device=True) as my_switch:
				#Configure DC Power Output
				'''
				my_smu.source_mode = nidcpower.SourceMode.SINGLE_POINT
				my_smu.output_function = nidcpower.OutputFunction.DC_VOLTAGE
				my_smu.voltage_level = 2.5
				my_smu.current_limit = 0.05
				my_smu.voltage_level_autorange = True
				my_smu.current_limit_autorange = True
				my_smu.source_delay = hightime.timedelta(seconds=0.1)
				'''
				my_smu.import_attribute_configuration_file('smu_config_ubuntu.nidcpowerconfig')
				#Start voltage generation in CH0
				print('Setting Power Supply CH0 to 2.5V ...')
				my_smu.initiate()
				my_smu.wait_for_event(nidcpower.Event.SOURCE_COMPLETE)

				measurements = my_smu.measure_multiple()
				print('Power Supply Measurements')
				print('  Voltage    Current')
				print(measurements[0].voltage, measurements[0].current)

				#Route DC Power CH0 to DMM
				start = time.perf_counter()
				my_switch.connect(channel1= 'ch0', channel2= 'com')
				end = time.perf_counter()
				route_a = (end - start) * 1000
				print('Channel CH0 and COM are now connected.')

				#Take DMM measurement
				start = time.perf_counter()
				my_dmm.configure_measurement_digits(nidmm.Function.DC_VOLTS, 10, 7.5)
				end = time.perf_counter()
				meas_1 = (end - start) * 1000
				print("Measurement: " + str(my_dmm.read()))

				#Disconnect CH0 and COM
				start = time.perf_counter()
				my_switch.disconnect(channel1= 'ch0', channel2= 'com')
				end = time.perf_counter()
				nroute_a = (end - start) * 1000
				print('Channel CH0 and COM are now disconnected.')

				time.sleep(3)

				#Route DMM to Short-Circuit
				print('Routing DMM to a short-circuited path ...')
				start = time.perf_counter()
				my_switch.connect(channel1= 'ch1', channel2= 'com')
				end = time.perf_counter()
				route_b = (end - start) * 1000
				print('Channel CH1 and COM are now connected.')

				#Take DMM measurement
				start = time.perf_counter()
				my_dmm.configure_measurement_digits(nidmm.Function.DC_VOLTS, 10, 7.5)
				end = time.perf_counter()
				meas_2 = (end - start) * 1000
				print("Measurement: " + str(my_dmm.read()))

				#Disconnect CH0 and COM
				start = time.perf_counter()
				my_switch.disconnect(channel1= 'ch1', channel2= 'com')
				end = time.perf_counter()
				nroute_b = (end - start) * 1000
				print('Channel CH1 and COM are now disconnected.')

				#Reset DC Power Session
				my_smu.reset()

				return route_a, route_b, nroute_a, nroute_b, meas_1, meas_2

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


start_t = time.perf_counter()
route_a, route_b, nroute_a, nroute_b, meas_1, meas_2 = route_meas()
end_t = time.perf_counter()
total_ex = (end_t -start_t)
display_rlts(route_a, route_b, nroute_a, nroute_b, meas_1, meas_2, total_ex)

