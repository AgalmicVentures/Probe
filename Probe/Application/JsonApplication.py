
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
import threading
import time

#Globals so their swaps will be atomic and not require locking
_hardware = {}
_status = {}

def jsonResponse(value):
	cherrypy.response.headers['Content-Type'] = 'application/json'
	return json.dumps(value, indent=4, sort_keys=True).encode('utf8')

class ProbeJsonApplication(object):

	def __init__(self):
		self._backgroundUpdate()

		self._backgroundThread = threading.Thread(target=self._backgroundThread)
		self._backgroundThread.daemon = True
		self._backgroundThread.start()

	def _backgroundThread(self):
		"""
		The background status checking thread.
		"""
		lastUpdate = datetime.datetime.now()
		while True:
			time.sleep(0.5)

			now = datetime.datetime.now()
			if lastUpdate is None or now - lastUpdate > datetime.timedelta(seconds=5):
				self._backgroundUpdate()
				lastUpdate = now

	def _backgroundUpdate(self):
		"""
		Updates the hardware and status information every 5 seconds.
		"""
		#Cache hardware
		bootTime = datetime.datetime.utcfromtimestamp(psutil.boot_time())
		cpuFrequency = psutil.cpu_freq()

		global _hardware
		_hardware = {
			'bootTime': bootTime.strftime('%Y-%m-%dT%H:%M:%SZ'),
			'cpuCores': psutil.cpu_count(),
			'cpuFrequencyMhz': None if cpuFrequency is None else {
				'current': cpuFrequency.current,
				'max': cpuFrequency.max,
				'min': cpuFrequency.min,
			},
			'isMac': os.uname().sysname == 'Darwin',
		}

		now = datetime.datetime.utcnow()
		battery = psutil.sensors_battery()
		cpuStats = psutil.cpu_stats()
		cpuTimes = psutil.cpu_times()
		virtualMemory = psutil.virtual_memory()
		swapMemory = psutil.swap_memory()
		diskIoCounters = psutil.disk_io_counters()
		network = psutil.net_io_counters()

		entropyAvailable = None
		try:
			with open('/proc/sys/kernel/random/entropy_avail') as entropyAvailableFile:
				entropyAvailable = int(entropyAvailableFile.read().strip())
		except (IOError, ValueError):
			pass

		global _status
		_status = {
			'time': now.strftime('%Y-%m-%d %H:%M:%S'),
			'uptime': int((now - bootTime).total_seconds()),
			'entropyAvailable': entropyAvailable,
			'battery': None if battery is None else {
				'percent': battery.percent,
				'pluggedIn': battery.power_plugged,
				'secsleft': battery.secsleft,
			},
			'cpuPercent': psutil.cpu_percent(interval=0.1),
			'cpuStats': {
				'contextSwitches': cpuStats.ctx_switches,
				'interrupts': cpuStats.interrupts,
				'softInterrupts': cpuStats.soft_interrupts,
				'syscalls': cpuStats.syscalls,
			},
			'cpuTimes': {
				'idle': cpuTimes.idle,
				'nice': cpuTimes.nice,
				'system': cpuTimes.system,
				'user': cpuTimes.user,
			},
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
			'diskIoCounters': {
				'readCount': diskIoCounters.read_count,
				'writeCount': diskIoCounters.write_count,
				'readBytes': diskIoCounters.read_bytes,
				'writeBytes': diskIoCounters.write_bytes,
				'readTime': diskIoCounters.read_time,
				'writeTime': diskIoCounters.write_time,
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
		}

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return jsonResponse({
			'error': 'API not found',
		})

	@cherrypy.expose
	def hardware(self):
		return jsonResponse(_hardware)

	@cherrypy.expose
	def status(self):
		return jsonResponse(_status)
