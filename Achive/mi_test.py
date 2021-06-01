import grpc
import time
import nidcpower_pb2 as nidcpower_types
import nidcpower_pb2_grpc as grpc_nidcpower
import niswitch_pb2 as niswitch_types
import niswitch_pb2_grpc as grpc_niswitch
import nidmm_pb2 as nidmm_types
import nidmm_pb2_grpc as grpc_nidmm

server_address = "CR-SJO-8840-IRZ"
server_port = "31763"

dc_session_name = "NI-DCPower-Session"
sw_session_name = "NI-Switch-Session-1"
dmm_session_name = "NI-DMM-Session"

# Device configuration variables.
dc_resource = "myDCPower"
dc_options = "Simulate=0,DriverSetup=Model:4110;BoardType:PXI"
dc_channels = "0"
sw_resource = "mySwitch"
topology_string = "2503/2-Wire 24x1 Mux"
dmm_resource = "myDMM"
dmm_options = "Simulate=0, DriverSetup=Model:4071; BoardType:PXI"

# Parameters
voltage_level = 2.5
config_range = 10.0
resolution = 5.5
measurementType = nidmm_types.Function.FUNCTION_NIDMM_VAL_DC_VOLTS
max_time = nidmm_types.TimeLimit.TIME_LIMIT_NIDMM_VAL_TIME_LIMIT_AUTO
simulation = False
reset_device = True

# Create the communication channel for the remote host and create connections to the NI dvice and session services.
channel = grpc.insecure_channel(f"{server_address}:{server_port}")
dc_client = grpc_nidcpower.NiDCPowerStub(channel)
sw_client = grpc_niswitch.NiSwitchStub(channel)
dmm_client = grpc_nidmm.NiDmmStub(channel)

# Checks for errors. If any, throws an exception to stop the execution.
any_error = False
def CheckForError (client, vi, status) :
    global any_error
    if(status != 0 and not any_error):
        any_error = True
        ThrowOnError (client, vi, status)

def ThrowOnError (client, vi, error_code):
    error_message_request = nidcpower_types.ErrorMessageRequest(
        vi = vi,
        error_code = error_code
        )
    error_message_response = client.ErrorMessage(error_message_request)
    raise Exception (error_message_response.error_message)

# Displays timing metrics
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

try:
    start_t = time.perf_counter()
	# [DC] Initialize the session.
    initialize_with_channels_response = dc_client.InitializeWithChannels(nidcpower_types.InitializeWithChannelsRequest(
        session_name = dc_session_name,
        resource_name = dc_resource,
        channels = dc_channels,
        reset = reset_device,
        option_string = dc_options
    ))
    dc_vi = initialize_with_channels_response.vi
    CheckForError(dc_client, dc_vi, initialize_with_channels_response.status)
	
	# [DC] Specify source mode.
    configure_source_mode = dc_client.SetAttributeViInt32(nidcpower_types.SetAttributeViInt32Request(
        vi = dc_vi,
        attribute_id = nidcpower_types.NiDCPowerAttributes.NIDCPOWER_ATTRIBUTE_SOURCE_MODE,
        attribute_value = nidcpower_types.SourceMode.SOURCE_MODE_NIDCPOWER_VAL_SINGLE_POINT
    ))
    CheckForError(dc_client, dc_vi, configure_source_mode.status)
	
	# [DC] Configure output function
    configure_output_function = dc_client.SetAttributeViInt32(nidcpower_types.SetAttributeViInt32Request(
        vi = dc_vi,
        attribute_id = nidcpower_types.NiDCPowerAttributes.NIDCPOWER_ATTRIBUTE_OUTPUT_FUNCTION,
        attribute_value = nidcpower_types.OutputFunction.OUTPUT_FUNCTION_NIDCPOWER_VAL_DC_VOLTAGE
    ))
    CheckForError(dc_client, dc_vi, configure_output_function.status)
	
	# [DC] Set the voltage level
    configure_voltage_level = dc_client.ConfigureVoltageLevel(nidcpower_types.ConfigureVoltageLevelRequest(
        vi = dc_vi,
        level = voltage_level
    ))
    CheckForError(dc_client, dc_vi, configure_voltage_level.status)
	
	# [SW] Open session to NI-SWITCH and set topology.
    init_with_topology_response = sw_client.InitWithTopology(niswitch_types.InitWithTopologyRequest(
        session_name = sw_session_name,
        resource_name = sw_resource,
        topology = topology_string,
        simulate = simulation,
        reset_device = reset_device
        ))
    sw_vi = init_with_topology_response.vi
    CheckForError(sw_client, sw_vi, init_with_topology_response.status)
    print("Topology set to : ",topology_string)
	
	# [DMM] Open session
    init_with_options_response = dmm_client.InitWithOptions(nidmm_types.InitWithOptionsRequest(
        session_name = dmm_session_name,
        resource_name = dmm_resource,
        id_query = False,
        option_string = dmm_options
    ))
    dmm_vi = init_with_options_response.vi
    CheckForError(dmm_client, dmm_vi, init_with_options_response.status)
	
	# [DMM] Configure measurement
    config_measurement_response = dmm_client.ConfigureMeasurementDigits(nidmm_types.ConfigureMeasurementDigitsRequest(
        vi = dmm_vi,
        measurement_function = measurementType,
        range = config_range,
        resolution_digits = resolution
    ))
    CheckForError(dmm_client, dmm_vi, config_measurement_response.status)
	
	# [DC] Initiate the session.
    initiate_response = dc_client.Initiate(nidcpower_types.InitiateRequest(
        vi = dc_vi,
    ))
    CheckForError(dc_client, dc_vi, initiate_response.status)
	
	# [DC] Wait for event (Source Complete)
    dc_event = nidcpower_types.ExportSignal.EXPORT_SIGNAL_NIDCPOWER_VAL_SOURCE_COMPLETE_EVENT
    wait_for_event = dc_client.WaitForEvent(nidcpower_types.WaitForEventRequest(
        vi = dc_vi,
        event_id = dc_event,
		timeout = 4,
    ))
    CheckForError(dc_client, dc_vi, wait_for_event.status)
	
	# [DC] Measure channel output
    measure_channel = dc_client.MeasureMultiple(nidcpower_types.MeasureMultipleRequest(
		vi = dc_vi,
		channel_name = dc_channels
    ))
    CheckForError(dc_client, dc_vi, measure_channel.status)
	
    print('Power Supply Measurements')
    print(measure_channel)
	
	# [SW] Connect CH0 to COM0
    start = time.perf_counter()
    CheckForError(sw_client, sw_vi, (sw_client.Connect(niswitch_types.ConnectRequest(
        vi = sw_vi,
        channel1 = "ch0",
        channel2 = "com0"
        ))).status)
    end = time.perf_counter()
    route_a = (end - start) * 1000
    print('Channel CH0 and COM0 are now connected.')
	
	# [DMM] Take measurement
    start = time.perf_counter()
    measure = dmm_client.Read(nidmm_types.ReadRequest(
		vi = dmm_vi,
		maximum_time = max_time
    ))
    CheckForError(dmm_client, dmm_vi, measure.status)
    end = time.perf_counter()
    meas_1 = (end - start) * 1000
    print('DMM Measurement:', str(measure.reading))
	
	# [SW] Disconnect CH0 to COM0
    start = time.perf_counter()
    CheckForError(sw_client, sw_vi, (sw_client.Disconnect(niswitch_types.DisconnectRequest(
        vi = sw_vi,
        channel1 = "ch0",
        channel2 = "com0"
        ))).status)
    end = time.perf_counter()
    nroute_a = (end - start) * 1000
    print('Channel CH0 and COM0 are now disconnected.')
	
	# [SW] Connect CH1 to COM0
    start = time.perf_counter()
    CheckForError(sw_client, sw_vi, (sw_client.Connect(niswitch_types.ConnectRequest(
        vi = sw_vi,
        channel1 = "ch1",
        channel2 = "com0"
        ))).status)
    end = time.perf_counter()
    route_b = (end - start) * 1000
    print('Channel CH1 and COM0 are now connected.')
	
	# [DMM] Take measurement
    start = time.perf_counter()
    measure = dmm_client.Read(nidmm_types.ReadRequest(
		vi = dmm_vi,
		maximum_time = max_time
    ))
    end = time.perf_counter()
    meas_2 = (end - start) * 1000
    CheckForError(dmm_client, dmm_vi, measure.status)
    print('DMM Measurement:', str(measure.reading))
	
	# [SW] Disconnect CH1 to COM0
    start = time.perf_counter()
    CheckForError(sw_client, sw_vi, (sw_client.Disconnect(niswitch_types.DisconnectRequest(
        vi = sw_vi,
        channel1 = "ch1",
        channel2 = "com0"
        ))).status)
    end = time.perf_counter()
    nroute_b = (end - start) * 1000
    print('Channel CH1 and COM0 are now disconnected.')

except grpc.RpcError as rpc_error:
    error_message = rpc_error.details()
    if rpc_error.code() == grpc.StatusCode.UNAVAILABLE :
        error_message = f"Failed to connect to server on {server_address}"
    elif rpc_error.code() == grpc.StatusCode.UNIMPLEMENTED:
        error_message = "The operation is not implemented or is not supported/enabled in this service"
    print(f"{error_message}")

finally:
    # [DC] Close the session.
    close_dc_session = dc_client.Close(nidcpower_types.CloseRequest(
            vi = dc_vi
        ))
    CheckForError(dc_client, dc_vi, close_dc_session.status)
	# [SW] Close the session.
    close_sw_session = sw_client.Close(niswitch_types.CloseRequest(
            vi = sw_vi
        ))
    CheckForError(sw_client, sw_vi, close_sw_session.status)
	# [DMM] Close session
    close_dmm_session = dmm_client.Close(nidmm_types.CloseRequest(
            vi = dmm_vi
        ))
    CheckForError(dmm_client, dmm_vi, close_dmm_session.status)

    end_t = time.perf_counter()
    total_ex = (end_t -start_t) * 1000

    display_rlts(route_a, route_b, nroute_a, nroute_b, meas_1, meas_2, total_ex)