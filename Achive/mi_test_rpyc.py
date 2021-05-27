#!/usr/bin/python

import hightime
import nidcpower
import niswitch
import nidaqmx
import time

def route_meas():
    SIMULATE = False

    print('Starting the program ...')

    with nidcpower.Session(resource_name='PXI1Slot2', channels='0') as dc_session:

        #Configure DC Power Session
        dc_session.simulate = SIMULATE
        dc_session.source_mode = nidcpower.SourceMode.SINGLE_POINT
        dc_session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        dc_session.voltage_level = 5.0
        dc_session.current_limit = 0.1
        dc_session.voltage_level_autorange = True
        dc_session.current_limit_autorange = True
        dc_session.source_delay = hightime.timedelta(seconds=0.1)

        #Initiate voltage generation
        print('Setting Power Supply CH0 to 5V ...')
        dc_session.initiate()
        dc_session.wait_for_event(nidcpower.Event.SOURCE_COMPLETE, hightime.timedelta(seconds=10))

        #Routes AI
        print('Routing AI to Power Supply CH0 ...')
        with niswitch.Session(resource_name='PXI1Slot5', topology='2503/2-wire 24x1 Mux', simulate=SIMULATE, reset_device=True) as sw_session:
            start = time.perf_counter()
            sw_session.connect(channel1= 'ch0', channel2= 'com0')
            end = time.perf_counter()
            print('Channel CH0 and COM0 are now connected. Task completed in', str(end-start),'seconds')
            #AI Read
            start = time.perf_counter()
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan("PXI1Slot3_2/ai0")
                reading = task.read()
                end = time.perf_counter()
                print('AI Measurement:', str(reading), 'Task completed in', str(end-start),'seconds')
            start = time.perf_counter()
            sw_session.disconnect(channel1= 'ch0', channel2= 'com0')
            end = time.perf_counter()
            print('Channel CH0 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')

            time.sleep(3)
            print('Routing AI to GND ...')
            start = time.perf_counter()
            sw_session.connect(channel1= 'ch1', channel2= 'com0')
            end = time.perf_counter()
            print('Channel CH1 and COM0 are now connected. Task completed in', str(end-start),'seconds')
            #AI Read
            start = time.perf_counter()
            with nidaqmx.Task() as task:
                task.ai_channels.add_ai_voltage_chan("PXI1Slot3_2/ai0")
                reading = task.read()
                end = time.perf_counter()
                print('AI Measurement:', str(reading), 'Task completed in', str(end-start),'seconds')
            start = time.perf_counter()
            sw_session.disconnect(channel1= 'ch1', channel2= 'com0')
            end = time.perf_counter()
            print('Channel CH1 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')

        print('Ending the program ...')

        #Close DC Power Session
        dc_session.reset()

start = time.perf_counter()
route_meas()
end = time.perf_counter()
print('Completed execution in', str(end-start),'seconds')
