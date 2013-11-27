#
# Hello World client in Python
# Connects REQ socket to tcp://localhost:5555
# Sends "Hello" to server, expects "World" back
#
import zmq
import json

SERVER_ADDRESS = "tcp://localhost:5955"

class Client:
	def __init__(self):
		self.context = zmq.Context()
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
		print "Recieved these services:"
		print services
	
	def connectToServer(self):
		socket = self.context.socket(zmq.REQ)
		socket.connect (SERVER_ADDRESS)
		return socket

client = Client()
client.getServices()