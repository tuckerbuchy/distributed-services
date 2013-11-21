#
# This is a service providing node. This node will register with the server all of its services, and then the server will keep 
# a map of all registered service providers with the services they provide. It will then open up a router connection at a server-specified port,
# and start to wait for requests to come in. When a request comes in it responds with the evaluated answer.
#
import zmq
import json

SERVER_ADDRESS = "tcp://localhost:5555"

class Service:
    def __init__(self, service_id, function):
        #this is the service id
        self.service_id = service_id  
        #this is a functor
        self.function = function

class ServiceProvidingNode:
    
    def __init__(self):
        self.context = zmq.Context()
        self.services = []
    
    def addService(self, service):
        self.services.append(service)
    
    def connectToServer(self, server_address):
        # Socket to talk to server
        print "Registering to server at ", server_address
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect (server_address)
        print "Connected."
    def formatRegisterRequest(self):
        registered_services = []
        for service in self.services:
            registered_services.append({"service_id":service.service_id})

        registered_str = json.dumps(registered_services)
        return registered_str
    def registerServices(self):
        reg_message = self.formatRegisterRequest()
        self.server_socket.send(reg_message)
        response = self.server_socket.recv()
        print response

def add(x,y):
    return x + y


def subtract(x,y):
    return x - y

service = ServiceProvidingNode()
service.addService(Service("add", add))
service.addService(Service("subtract", subtract))
service.connectToServer(SERVER_ADDRESS)
service.registerServices()