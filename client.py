#
# Hello World client in Python
# Connects REQ socket to tcp://localhost:5955
# Sends "Hello" to server, expects "World" back
#
import zmq
import json

SERVER_ADDRESS = "tcp://localhost:5995"

class Client:
	def __init__(self):
		self.context = zmq.Context()
		self.services_available = []
		while True:
			first_in = raw_input("Enter 'get_services' to get services available, or else enter the service id you wish to call.\n")
			if first_in == 'get_services':
				self.getServices()
			else:
				service_id = first_in
				args_str = raw_input("Enter service args, deliminated by comma (ex. 1,2,3):")
				args = args_str.split(',')
				#call the service.
				self.findService(service_id, args)

	def getServices(self):
		# Socket to talk to server
		print "Connecting to server at " + SERVER_ADDRESS
		socket = self.connectToServer();
		print "Connected."
		print "Querying available services...."
		service_request_json = {"services_request":"true"}
		service_request = json.dumps(service_request_json)
		socket.send(service_request)
		services = socket.recv()
		self.services_available = json.loads(services)
		print "Recieved these services:"
		for service_prov in self.services_available:
			services = service_prov["services"]
			for service in services:
				print "\t\t" + service
	
	def connectToServer(self):
		socket = self.context.socket(zmq.REQ)
		socket.connect (SERVER_ADDRESS)
		return socket

	def startPrompt(self):
		service_id = raw_input("Enter service you want to call:")
		args_str = raw_input("Enter args, deliminated by comma (ex. 1,2,3):")
		#convert the input to an array
		args = args_str.split(',')

	def findService(self, service_id, args):
		for service_list in self.services_available:
			if service_id in service_list["services"]:
				service_address = service_list["address"]
				self.callService(service_id, args, service_address)
	def callService(self, service_id, args, service_address):
		print "Connecting to service provider..." + service_address
		socket = self.context.socket(zmq.REQ)
		socket.connect(service_address)
		print "Connected."
		print "Calling service..."
		service_call = {"service_id":service_id, "args":args}
		service_call_message = json.dumps(service_call)
		socket.send(service_call_message)
		result = socket.recv()
		result_json = json.loads(result)
		print "##########################\nRecieved the result: " + result_json["result"] + "\n##########################"

client = Client()