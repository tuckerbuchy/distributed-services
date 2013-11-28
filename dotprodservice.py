from service import *
import numpy

def dotproduct(x, y):
	#have to convert from unicode to string to use the array conversion function
	x_str = x.encode("ascii")
	y_str = y.encode("ascii")

	#convert to a numpy vector
	x_v = numpy.fromstring(x)
	y_v = numpy.fromstring(y)
	return numpy.dot(x_v, y_v)

service = ServiceProvidingNode()
service.addService(Service("dotProduct", dotproduct))
service.connectToRegistryServer(SERVER_ADDRESS)
service.registerServices()