from service import *
import numpy

def dotproduct(x, y):
	#have to convert from unicode to string to use the array conversion function
	try:
		x_str = x.encode("ascii")
		y_str = y.encode("ascii")
		x_v = json.loads(x)
		y_v = json.loads(y)
		return numpy.dot(x_v, y_v)
	except ValueError:
		return "Invalid arguments!"
service = ServiceProvidingNode()
service.addService(Service("dotProduct", dotproduct))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()