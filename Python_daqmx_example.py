import rpyc

HOSTNAME = 'rscd27-Precision-T3610'
PORT = 18861

connection = rpyc.connect(HOSTNAME, PORT)
nidaqmx = connection.root.nidmm

system = nidaqmx.system.System.local()
system.driver_version
for device in system.devices:
	print("Detected board: -> " + str(device.product_type))
	print("Available channels -> " + str(device.ai_physical_chans))
with nidaqmx.Task() as task:
	print("Get Measurement...")
	task.ai_channels.add_ai_voltage_chan("PXI1Slot4/ai0")
	task.read()


