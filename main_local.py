import hightime
import nidcpower
import niswitch
import nidmm
import time

def route_meas():
    SIMULATE = False

    print('Starting the program ...')
    with nidcpower.Session(resource_name='DCPower', channels='0') as dc1_session: #SET RESOURCE NAME AND CHANNEL

        #Configure DC Power Session 1
        dc1_session.simulate = SIMULATE
        dc1_session.source_mode = nidcpower.SourceMode.SINGLE_POINT
        dc1_session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
        dc1_session.voltage_level = 2.5
        dc1_session.current_limit = 0.1
        dc1_session.voltage_level_autorange = True
        dc1_session.current_limit_autorange = True
        dc1_session.source_delay = hightime.timedelta(seconds=0.1)

        #Initiate voltage generation in session 1
        print('Setting Power Supply CH0 to 2.5V ...')
        dc1_session.initiate()
        dc1_session.wait_for_event(nidcpower.Event.SOURCE_COMPLETE, hightime.timedelta(seconds=10))

        with nidcpower.Session(resource_name='DCPower', channels='1') as dc2_session: #SET RESOURCE NAME AND CHANNEL

            #Configure DC Power Session 2
            dc2_session.simulate = SIMULATE
            dc2_session.source_mode = nidcpower.SourceMode.SINGLE_POINT
            dc2_session.output_function = nidcpower.OutputFunction.DC_VOLTAGE
            dc2_session.voltage_level = 5.0
            dc2_session.current_limit = 0.1
            dc2_session.voltage_level_autorange = True
            dc2_session.current_limit_autorange = True
            dc2_session.source_delay = hightime.timedelta(seconds=0.1)

            #Initiate voltage generation
            print('Setting Power Supply CH1 to 5V ...')
            dc2_session.initiate()
            dc2_session.wait_for_event(nidcpower.Event.SOURCE_COMPLETE, hightime.timedelta(seconds=10))

            #Routes DMM
            print('Routing DMM to Power Supply CH0 ...')
            with niswitch.Session(resource_name= 'Switch', topology= '2503/2-wire 24x1 Mux', simulate= SIMULATE, reset_device= True) as sw_session: #SET RESOURCE NAME
                start = time.perf_counter()
                sw_session.connect(channel1= 'ch0', channel2= 'com0')
                end = time.perf_counter()
                print('Channel CH0 and COM0 are now connected. Task completed in', str(end-start),'seconds')
                #DMM Read
                start = time.perf_counter()
                with nidmm.Session(resource_name = 'DMM', options = {'simulate': SIMULATE, 'driver_setup': {'Model': '4072', 'BoardType': 'PXI', }, }) as dmm_session: #SET RESOURCE NAME
                    dmm_session.configure_measurement_digits(measurement_function = nidmm.Function.DC_VOLTS, range = 10, resolution_digits = 6.5)
                    reading = dmm_session.read()
                    end = time.perf_counter()
                    print('DMM Measurement:', str(reading), 'Task completed in', str(end-start),'seconds')
                start = time.perf_counter()
                sw_session.disconnect(channel1= 'ch0', channel2= 'com0')
                end = time.perf_counter()
                print('Channel CH0 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')
                time.sleep(3)
                print('Routing DMM to CH1 ...')
                start = time.perf_counter()
                sw_session.connect(channel1= 'ch1', channel2= 'com0')
                end = time.perf_counter()
                print('Channel CH1 and COM0 are now connected. Task completed in', str(end-start),'seconds')
                #DMM Read
                start = time.perf_counter()
                with nidmm.Session(resource_name = 'DMM', options = {'simulate': SIMULATE, 'driver_setup': {'Model': '4072', 'BoardType': 'PXI', }, }) as dmm_session: #SET RESOURCE NAME
                    dmm_session.configure_measurement_digits(measurement_function = nidmm.Function.DC_VOLTS, range = 10, resolution_digits = 6.5)
                    reading = dmm_session.read()
                    end = time.perf_counter()
                    print('DMM Measurement:', str(reading), 'Task completed in', str(end-start),'seconds')
                start = time.perf_counter()
                sw_session.disconnect(channel1= 'ch1', channel2= 'com0')
                end = time.perf_counter()
                print('Channel CH1 and COM0 are now disconnected. Task completed in', str(end-start),'seconds')

            print('Ending the program ...')

            #Close DC Power Session 2
            dc2_session.reset()
        #Close DC Power Session 1
        dc1_session.reset()

start = time.perf_counter()
route_meas()
end = time.perf_counter()
print('Completed program execution in', str(end-start),'seconds')