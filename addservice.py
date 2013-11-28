from service import *

def add(x,y):
    return int(x) + int(y)

service = ServiceProvidingNode()
service.addService(Service("add", add))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()