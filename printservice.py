from service import *

printString = lambda x: x

service = ServiceProvidingNode()
service.addService(Service("printString", printString))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()