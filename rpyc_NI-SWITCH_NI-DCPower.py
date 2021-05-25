# Import libraries
import rpyc # python3 -m pip install rpyc
import nidcpower # python3 -m pip install dcpower
import niswitch # python3 -m pip install niswitch

# Import rpyc thread server
from rpyc.utils.server import ThreadedServer

# Declare NI-SWITCH rpyc service
class NI_SWTICH_service(rpyc.Service):
   exposed_niswitch = niswitch

# Declare NI-DCPower rpyc service
class NI_DCPower_service(rpyc.Service):
   exposed_nidcpower = nidcpower

# Declare Ports
NI_SWTICH_port = 18861
NI_DCPower_port = 18862

# Main code
if __name__ == "__main__":
	print("Starting NI-SWITCH and NI-DCPower rpyc service")
	t1 = ThreadedServer(NI_SWTICH_service, port = NI_SWTICH_port , protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t2 = ThreadedServer(NI_DCPower_service, port = NI_DCPower_port, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t1.start()
	t2.start()
	print("Press Ctrl+C to stop this service")
