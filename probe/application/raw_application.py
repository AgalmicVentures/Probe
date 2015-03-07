
import cherrypy
import subprocess

def getOutput(command):
	return subprocess.Popen(command.split(' '), stdout=subprocess.PIPE).communicate()[0]

class ProbeRawApplication:

	def __init__(self):
		#TODO
		pass

	@cherrypy.expose
	def index(self):
		return '<html><body><h1>Probe - Raw API</h1></body></html>'

	@cherrypy.expose
	def df(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('df -h')

	@cherrypy.expose
	def ifconfig(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('ifconfig')

	@cherrypy.expose
	def iostat(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('iostat')

	@cherrypy.expose
	def uptime(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('uptime')
