#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time
import json        
import socket

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
			server_query = self.services_socket.recv()

			# decode the json
			decoded_server_query = json.loads(server_query)

			if "services_request" in decoded_server_query:
				#send the services, this is a serviceconsumer
				self.services_socket.send(req_id, zmq.SNDMORE)
				self.services_socket.send(empty, zmq.SNDMORE)
				self.services_socket.send(json.dumps(self.advertised_services))
			elif "address" in decoded_server_query:
				#this means that we are dealing with a provider
				self.services_socket.send(req_id, zmq.SNDMORE)
				self.services_socket.send(empty, zmq.SNDMORE)
				self.services_socket.send_string("Registered you @ " + decoded_server_query["address"])

				print "Recieved services : " + server_query
				print "Registering..."
					
				self.advertised_services.append(decoded_server_query)
				print "Registered.\n"

#start the server
server = RegistryServer("tcp://*:5995")
