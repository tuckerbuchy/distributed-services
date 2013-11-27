from service import *

def add(x,y):
    return x + y

service = ServiceProvidingNode()
service.addService(Service("add", add))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()