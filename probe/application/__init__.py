
import cherrypy

import application.json_application
import application.raw_application

class ProbeApplication:

	def __init__(self):
		self.json = json_application.ProbeJsonApplication()
		self.raw = raw_application.ProbeRawApplication()
		#TODO: human interface

	@cherrypy.expose
	def index(self):
		return '<html><body><h1>Probe</h1></body></html>'

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return '<html><body><h1>Probe - Page Not Found</h1></body></html>'
