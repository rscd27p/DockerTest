# Import libraries
import rpyc # python3 -m pip install rpyc
import nidcpower # python3 -m pip install dcpower
import niswitch # python3 -m pip install niswitch
import nidmm #  python3 -m pip install nidmm

# Import rpyc thread server
from rpyc.utils.server import ThreadedServer

# Declare NI-SWITCH rpyc service
class NI_SWTICH_service(rpyc.Service):
   exposed_niswitch = niswitch
   print("NI-SWITCH thread started...")

# Declare NI-DCPower rpyc service
class NI_DCPower_service(rpyc.Service):
   exposed_nidcpower = nidcpower
   print("NI-DCPower thread started...")
   
# Declare NI-DCPower rpyc service
class NI_DMM_service(rpyc.Service):
   exposed_nidmm = nidmm
   print("NI-DMM thread started...")

# Declare Ports
NI_SWTICH_port = 18861
NI_DCPower_port = 18862
NI_DMM_port = 18863

# Main code
if __name__ == "__main__":
	print("Starting NI-SWITCH and NI-DCPower rpyc service")
	print("Press Ctrl+C to stop this service")
	t1 = ThreadedServer(NI_SWTICH_service, port = NI_SWTICH_port , protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t2 = ThreadedServer(NI_DCPower_service, port = NI_DCPower_port, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t3 = ThreadedServer(NI_DMM_service, port = NI_DMM_port, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
	t1.start()
	t2.start()
	t3.start()
	print("Press Ctrl+C to stop this service")
