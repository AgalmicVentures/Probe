
import cherrypy
import json

class ProbeJsonApplication:

	def __init__(self):
		#TODO
		pass

	@cherrypy.expose
	def hardware(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'TODO': True,
		}).encode('utf8')

	@cherrypy.expose
	def software(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'TODO': True,
		}).encode('utf8')

	@cherrypy.expose
	def status(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'TODO': True,
		}).encode('utf8')
