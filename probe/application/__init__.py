
import cherrypy
import io
import socket

import application.json_application
import application.raw_application

class ProbeApplication:

	def __init__(self):
		self.json = json_application.ProbeJsonApplication()
		self.raw = raw_application.ProbeRawApplication()

		with io.open('./templates/index.html') as indexTemplateFile:
			self.indexTemplate = indexTemplateFile.read()

		self.hostname = socket.gethostname()

	@cherrypy.expose
	def index(self):
		return self.indexTemplate % {
			'hostname': self.hostname,
		}

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return '<html><body><h1>Probe - Page Not Found</h1></body></html>'
