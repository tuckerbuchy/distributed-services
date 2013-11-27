#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time
import json

class RegistryServer:
	def __init__(self, server_address):
		self.context = zmq.Context()
		self.server_address = server_address
		#bind to a socket.
		print "Binding to " + server_address + "..."
		self.services_socket = self.context.socket(zmq.ROUTER)
		self.services_socket.bind(server_address)
		
		#create place to store services
		self.advertised_services = []
		print "Ready to accept registrations"
		self.run()
	def run(self):
		while True:
			req_id = self.services_socket.recv()
			empty = self.services_socket.recv()
			registration = self.services_socket.recv()

			print "REQ_ID : " + str(req_id)
			print "REGISTRATION : " + registration
			port = 5577
			address = "tcp://*:" + str(port)

			self.services_socket.send(req_id, zmq.SNDMORE)
			self.services_socket.send(empty, zmq.SNDMORE)
			self.services_socket.send(address)

			print "Recieved services : " + registration
			print "Registering..."
				
			# decode the json
			decoded_services = json.loads(registration)
			self.advertised_services.append({"address":address, "services":decoded_services})
			print "Registered.\n"
			print "Current available services: \n\t\t" + json.dumps(self.advertised_services)
#start the server
server = RegistryServer("tcp://*:5555")
