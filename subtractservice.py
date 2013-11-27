from service import *

def subtract(x,y):
    return x - y

service = ServiceProvidingNode()
service.addService(Service("subtract", subtract))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()