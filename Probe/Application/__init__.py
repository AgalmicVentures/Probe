
# Copyright (c) 2015-2018 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import cherrypy
import io
import socket

import Application.ApiApplication

class ProbeApplication(object):

	def __init__(self):
		self.api = ApiApplication.ProbeApiApplication()

		with io.open('./templates/index.html') as indexTemplateFile:
			self._indexTemplate = indexTemplateFile.read()

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
