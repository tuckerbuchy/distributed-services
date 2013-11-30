from service import *

#this is a simple add service. This will returned the added result of two integers.

def add(x,y):
    return int(x) + int(y)

service = ServiceProvidingNode()
service.addService(Service("add", add))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()