
import cherrypy
import os
import subprocess

def getOutput(command):
	return subprocess.Popen(command.split(' '), stdout=subprocess.PIPE).communicate()[0]

def htmlEncode(s):
	return s.decode('utf-8').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&squot;')

def commandResponse(command):
	cherrypy.response.headers['Content-Type'] = 'text/plain'
	return htmlEncode(getOutput(command))

class ProbeRawApplication(object):

	def __init__(self):
		self._isMac = os.uname().sysname == 'Darwin'

	@cherrypy.expose
	def date(self):
		return commandResponse('date')

	@cherrypy.expose
	def df(self):
		return commandResponse('df -h')

	@cherrypy.expose
	def gitLog(self):
		return commandResponse('git log --graph -10')

	@cherrypy.expose
	def gitRevision(self):
		return commandResponse('git rev-parse HEAD')

	@cherrypy.expose
	def ifconfig(self):
		return commandResponse('/sbin/ifconfig')

	@cherrypy.expose
	def iostat(self):
		return commandResponse('iostat')

	@cherrypy.expose
	def mount(self):
		return commandResponse('mount')

	@cherrypy.expose
	def netstatTcp(self):
		return commandResponse('netstat -s -p tcp' if self._isMac else 'netstat -s -t')

	@cherrypy.expose
	def netstatUdp(self):
		return commandResponse('netstat -s -p udp' if self._isMac else 'netstat -s -u')

	@cherrypy.expose
	def numactlHardware(self):
		return commandResponse('numactl -h') if not self._isMac else 'numactl not available on Mac'

	@cherrypy.expose
	def uname(self):
		return commandResponse('uname -a')

	@cherrypy.expose
	def update(self):
		return commandResponse('git pull')

	@cherrypy.expose
	def uptime(self):
		return commandResponse('uptime')
