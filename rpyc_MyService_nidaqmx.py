import rpyc
import nidaqmx

class MyService(rpyc.Service):
   exposed_nidaqmx = nidaqmx

if __name__ == "__main__":
	from rpyc.utils.server import ThreadedServer
	t = ThreadedServer(MyService, port = 18861, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	print("Exporting NI-DAQmx...")
	t.start()
