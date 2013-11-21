#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time
import json

class Server:
	def __init__(self, server_address):
		self.context = zmq.Context()
		
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
			registration = self.services_socket.recv()
			
			#total hack, turns out that there is like a empty frame sent 
			#from the req on open, and it works when registrations length is greater than 5
			if  len(registration) > 5:
				print "Received request for " + registration + " to be registered."
				
				print "Registering..."
				
				#TODO: need to randomly generate ports
				port = "5577"
				
				#decode the json
				decoded_services = json.loads(registration)
				self.advertised_services.append({"port":port, "services":decoded_services})
				
				print "Registered on port " + port
				print "All provided services \n" + json.dumps(self.advertised_services)
				 
				self.services_socket.send(port)

#start the server
server = Server("tcp://*:5555")