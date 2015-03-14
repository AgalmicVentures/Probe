
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

		with io.open('./templates/configuration.html') as configurationTemplateFile:
			self.configurationTemplate = configurationTemplateFile.read()

		with io.open('./templates/help.html') as helpTemplateFile:
			self.helpTemplate = helpTemplateFile.read()

		with io.open('./templates/admin.html') as adminTemplateFile:
			self.adminTemplate = adminTemplateFile.read()

		self.hostname = socket.gethostname()

	@cherrypy.expose
	def index(self):
		return self.indexTemplate % {
			'hostname': self.hostname,
		}

	@cherrypy.expose
	def configuration(self):
		return self.configurationTemplate % {
			'hostname': self.hostname,
		}

	@cherrypy.expose
	def help(self):
		return self.helpTemplate % {
			'hostname': self.hostname,
		}

	@cherrypy.expose
	def admin(self):
		return self.adminTemplate % {
			'hostname': self.hostname,
		}

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return '<html><body><h1>Probe - Page Not Found</h1></body></html>'
