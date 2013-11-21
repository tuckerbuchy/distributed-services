#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects "Hello" from client, replies with "World"
#
import zmq
import time
import json

context = zmq.Context()

#This is the socket we connect a sample client too, that will send some request over.
socket_for_client = context.socket(zmq.REP)
socket_for_client.bind("tcp://*:5555")

#register the sockets for what the server should poll
poller = zmq.Poller()
poller.register(socket_for_client, zmq.POLLIN)

while True:
	socks = dict(poller.poll())

	if socket_for_client in socks and socks[socket_for_client] == zmq.POLLIN:
		message = socket_for_client.recv()
		response = message;
		#json_message = json.loads(message)
		#response = "Registered ", json_message[0]['methodname']
     	time.sleep (1)
     	socket_for_client.send(response)