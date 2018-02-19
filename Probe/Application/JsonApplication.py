
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
import datetime
import json
import os
import psutil

def jsonResponse(value):
	cherrypy.response.headers['Content-Type'] = 'application/json'
	return json.dumps(value, indent=4, sort_keys=True).encode('utf8')

class ProbeJsonApplication(object):

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return jsonResponse({
			'error': 'API not found',
		})

	@cherrypy.expose
	def hardware(self):
		return jsonResponse({
			'bootTime': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
			'cpuCores': psutil.NUM_CPUS,
			'isMac': os.uname().sysname == 'Darwin',
			'ram': psutil.TOTAL_PHYMEM,
		})

	@cherrypy.expose
	def status(self):
		bootTime = datetime.datetime.fromtimestamp(psutil.boot_time())
		now = datetime.datetime.now()

		virtualMemory = psutil.virtual_memory()
		swapMemory = psutil.swap_memory()
		network = psutil.net_io_counters()

		entropyAvailable = None
		try:
			with open('/proc/sys/kernel/random/entropy_avail') as entropyAvailableFile:
				entropyAvailable = int(entropyAvailableFile.read().strip())
		except (IOError, ValueError):
			pass

		return jsonResponse({
			'time': now.strftime('%Y-%m-%d %H:%M:%S'),
			'uptime': int((now - bootTime).total_seconds()),
			'entropyAvailable': entropyAvailable,
			'cpuPercent': psutil.cpu_percent(interval=0.1),
			'virtualMemory': {
				'total': virtualMemory.total,
				'available': virtualMemory.available,
				'percent': virtualMemory.percent,
				'used': virtualMemory.used,
				'free': virtualMemory.free,
			},
			'swapMemory': {
				'total': swapMemory.total,
				'used': swapMemory.used,
				'free': swapMemory.free,
				'percent': swapMemory.percent,
				'in': swapMemory.sin,
				'out': swapMemory.sout,
			},
			'network': {
				'bytesSent': network.bytes_sent,
				'bytesReceived': network.bytes_recv,
				'packetsSent': network.packets_sent,
				'packetsReceived': network.packets_recv,
				'errorIn': network.errin,
				'errorOut': network.errout,
				'droppedIn': network.dropin,
				'droppedOut': network.dropout,
			},
		})
