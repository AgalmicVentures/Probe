
import cherrypy

class ProbeJsonApplication:

	def __init__(self):
		#TODO
		pass

	@cherrypy.expose
	def index(self):
		return '<html><body><h1>Probe - JSON API</h1></body></html>'
