
import cherrypy
import io
import socket

import Application.JsonApplication
import Application.RawApplication

class ProbeApplication:

	def __init__(self):
		self.json = JsonApplication.ProbeJsonApplication()
		self.raw = RawApplication.ProbeRawApplication()

		with io.open('./templates/index.html') as indexTemplateFile:
			self._indexTemplate = indexTemplateFile.read()

		with io.open('./templates/configuration.html') as configurationTemplateFile:
			self._configurationTemplate = configurationTemplateFile.read()

		with io.open('./templates/help.html') as helpTemplateFile:
			self._helpTemplate = helpTemplateFile.read()

		with io.open('./templates/admin.html') as adminTemplateFile:
			self._adminTemplate = adminTemplateFile.read()

		self._hostname = socket.gethostname()

	@cherrypy.expose
	def index(self):
		return self._indexTemplate % {
			'hostname': self._hostname,
			'title': 'Status',
		}

	@cherrypy.expose
	def configuration(self):
		return self._configurationTemplate % {
			'hostname': self._hostname,
			'title': 'Configuration',
		}

	@cherrypy.expose
	def help(self):
		return self._helpTemplate % {
			'hostname': self._hostname,
			'title': 'Help',
		}

	@cherrypy.expose
	def admin(self):
		return self._adminTemplate % {
			'hostname': self._hostname,
			'title': 'Admin',
		}

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return '<html><body><h1>Probe - Page Not Found</h1></body></html>'
