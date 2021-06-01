# Import libraries
import rpyc # python3 -m pip install rpyc
import nidcpower # python3 -m pip install dcpower
import niswitch # python3 -m pip install niswitch
import nidmm #  python3 -m pip install nidmm

# Import rpyc thread server
from rpyc.utils.server import ThreadedServer

# Declare NI-SWITCH rpyc service
class NI_service(rpyc.Service):
   exposed_niswitch = niswitch
   print("NI-SWITCH thread started...")
   exposed_nidmm = nidmm
   print("NI-DMM thread started...")
   exposed_nidcpower = nidcpower
   print("NI-DCPower thread started...")

# Declare Ports
NI_rpyc_port = 18861


# Main code
if __name__ == "__main__":
	print("Starting NI-SWITCH, NI-DMM and NI-DCPower rpyc service")
	print("Press Ctrl+C to stop this service")
	t1 = ThreadedServer(NI_service, port = NI_rpyc_port, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t1.start()
	print("Press Ctrl+C to stop this service")
