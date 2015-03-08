
import cherrypy
import os
import subprocess

def getOutput(command):
	return subprocess.Popen(command.split(' '), stdout=subprocess.PIPE).communicate()[0]

class ProbeRawApplication:

	def __init__(self):
		self.isMac = os.uname().sysname == 'Darwin'

	@cherrypy.expose
	def index(self):
		return '<html><body><h1>Probe - Raw API</h1></body></html>'

	@cherrypy.expose
	def date(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('date')

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
	def netstatTcp(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('netstat -s -p tcp' if self.isMac else 'netstat -s -t')

	@cherrypy.expose
	def netstatUdp(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('netstat -s -p udp' if self.isMac else 'netstat -s -u')

	@cherrypy.expose
	def uname(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('uname -a')

	@cherrypy.expose
	def uptime(self):
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return getOutput('uptime')
