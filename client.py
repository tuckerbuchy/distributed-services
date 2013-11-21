#
# Hello World client in Python
# Connects REQ socket to tcp://localhost:5555
# Sends "Hello" to server, expects "World" back
#
import zmq
import json

#class to format messages to json over the wire.
class MessageFormatter:
	def getRegisterMessage(self, method_name, num_args):
		#build the message
		register_message = [{'methodname':method_name, 'numargs':num_args}]
		#convert to string
		register_message_str = json.dumps(register_message)
		return register_message_str

server_address = "tcp://localhost:5555"

context = zmq.Context()

# Socket to talk to server
print "Connecting to server at ", server_address
socket = context.socket(zmq.REQ)
socket.connect (server_address)
print "Connected."

print "Registering service..."
formatter = MessageFormatter()
reg_message = formatter.getRegisterMessage("add", 2)
socket.send(reg_message)
response = socket.recv()
#wait for response
print response

# # Do 10 requests, waiting each time for a response
# while True:
# 	print "Sending request "
# 	socket.send ("Registering service: Add1")
# 
# 	# Get the reply.
# 	message = socket.recv()
# 	print "Received reply ", "[", message, "]"