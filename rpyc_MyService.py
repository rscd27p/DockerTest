import rpyc
import nidmm

class MyService(rpyc.Service):
   exposed_nidmm = nidmm

if __name__ == "__main__":
   from rpyc.utils.server import ThreadedServer
   t = ThreadedServer(MyService, port = 18861, protocol_config = {"allow_public_attrs" : True, "allow_all_attrs" : True})
   t.start()