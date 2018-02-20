
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
	def entropyAvail(self):
		return commandResponse('cat /proc/sys/kernel/random/entropy_avail')

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
		return commandResponse('numactl -H') if not self._isMac else 'numactl not available on Mac'

	@cherrypy.expose
	def uname(self):
		return commandResponse('uname -a')

	@cherrypy.expose
	def update(self):
		return commandResponse('git pull')

	@cherrypy.expose
	def uptime(self):
		return commandResponse('uptime')
