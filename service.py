#
# This is a service providing node. This node will register with the server all of its services, and then the server will keep 
# a map of all registered service providers with the services they provide. It will then open up a router connection at a server-specified port,
# and start to wait for requests to come in. When a request comes in it responds with the evaluated answer.
#
import zmq
import json
import uuid
import socket

SERVER_ADDRESS = "tcp://localhost:5995"

class Service:
    def __init__(self, service_id, function):
        #this is the service id
        self.service_id = service_id
        #this is a functor
        self.function = function

def getOpenPort():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(("",0))
	s.listen(1)
	port = s.getsockname()[1]
	s.close()
	return port

class ServiceProvidingNode:
    
    def __init__(self):
        self.context = zmq.Context()
        self.services = []
        
        #we identify ourselves with a uuid.
        self.id = uuid.uuid1()
    
    def addService(self, service):
        self.services.append(service)
    
    def connectToRegistryServer(self, server_address):
        # Socket to talk to server
        print "Registering to server at ", server_address
        self.server_socket = self.context.socket(zmq.REQ)
        self.server_socket.connect (server_address)
        print "Connected."

    def formatRegisterRequest(self):
        registered_services = []
        for service in self.services:
            registered_services.append(service.service_id)
        registration_json = {}

        port = getOpenPort()

        address = "tcp://127.0.1.1:%d" %(port)
        registration_json["address"] = address
        registration_json["services"] = registered_services
        return registration_json
	
    #registers the services by sending a request over the wire, letting the server know it exists.
    def registerServices(self):
        registration_json = self.formatRegisterRequest()
        registered_str = json.dumps(registration_json)
        self.server_socket.send(registered_str)
        registration_confirmation = self.server_socket.recv()
        print registration_confirmation

        net_address = registration_json["address"]
        self.openServiceSocket(net_address)
        
    def openServiceSocket(self, net_address):
        print "Opening on  " + net_address + " for any incoming requests..."
        self.services_socket = self.context.socket(zmq.ROUTER)
        self.services_socket.bind(net_address)
        #wait on this socket now..
        print "Listening on services socket @ %s" %(net_address)
        while True:
            req_id = self.services_socket.recv()
            empty = self.services_socket.recv()
            #this is the actual service request object.
            message = self.services_socket.recv()
            service_request = json.loads(message)
            result = self.processRequest(service_request)
            result = {}
            result["result"] = result
            result_str = json.dumps(result)
            self.services_socket.send(req_id, zmq.SNDMORE)
            self.services_socket.send("", zmq.SNDMORE)
            self.services_socket.send(result_str)

    def processRequest(self, service_request):
    	service_id = service_request["service_id"]
    	for service in self.services:
    		if service.service_id == service_id:
    			fun = service.function
    			args = service_request["args"]
    			#this calls the function with the array parameters
    			return fun(*args)
    	return "No service exists!"

