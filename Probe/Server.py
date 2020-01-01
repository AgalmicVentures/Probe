#!/usr/bin/env python3

# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
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

import argparse
import datetime
import flask
import io
import psutil
import socket
import sys
import threading
import time

#Make sure the path is set up
import inspect
import os
_currentFile = os.path.abspath(inspect.getfile(inspect.currentframe()))
_currentDir = os.path.dirname(_currentFile)
_parentDir = os.path.dirname(_currentDir)
sys.path.append(_parentDir)

app = flask.Flask('Probe',
	static_url_path='/assets',
	template_folder=os.path.join(_parentDir, 'templates'))

_hostname = socket.gethostname()

#Global so the swaps will be atomic and not require locking
_status = {}

def _backgroundUpdate():
	"""
	Updates the hardware and status information every 5 seconds.
	"""
	#Cache hardware
	bootTime = datetime.datetime.utcfromtimestamp(psutil.boot_time())
	cpuFrequency = psutil.cpu_freq()
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

	#This swap is atomic, so no locking is required. Disassembling with `dis.dis`:
	#        436 BUILD_CONST_KEY_MAP     16
	#        438 STORE_GLOBAL            61 (_status)  <--- one atomic operation
	#        440 LOAD_CONST               1 (None)
	#        442 RETURN_VALUE
	global _status
	_status = {
		'hostname': _hostname,
		'isMac': os.uname().sysname == 'Darwin',

		'time': now.strftime('%Y-%m-%d %H:%M:%S'),
		'bootTime': bootTime.strftime('%Y-%m-%dT%H:%M:%SZ'),
		'uptime': int((now - bootTime).total_seconds()),
		'entropyAvailable': entropyAvailable,

		'battery': None if battery is None else {
			'percent': battery.percent,
			'pluggedIn': battery.power_plugged,
			'secsleft': battery.secsleft,
		},
		'cpuCores': psutil.cpu_count(),
		'cpuFrequencyMhz': None if cpuFrequency is None else {
			'current': cpuFrequency.current,
			'max': cpuFrequency.max,
			'min': cpuFrequency.min,
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
			'bytesReceived': network.bytes_recv,
			'bytesSent': network.bytes_sent,
			'packetsReceived': network.packets_recv,
			'packetsSent': network.packets_sent,
			'errorsIn': network.errin,
			'errorsOut': network.errout,
			'dropsIn': network.dropin,
			'dropsOut': network.dropout,
		},
	}

def _backgroundThread():
	"""
	The background status checking thread.
	"""
	lastUpdate = datetime.datetime.now()
	while True:
		time.sleep(0.5)

		now = datetime.datetime.now()
		if lastUpdate is None or now - lastUpdate > datetime.timedelta(seconds=5):
			_backgroundUpdate()
			lastUpdate = now

@app.route('/')
def index():
	return flask.render_template('index.html',
		hostname=_hostname,
		title='Status',
	)

@app.route('/help')
def help():
	return flask.render_template('help.html',
		hostname=_hostname,
		title='Help',
	)

@app.errorhandler(404)
def default(*args, **kwargs):
	return flask.Response(
		'<html><body><h1>Probe - Page Not Found</h1></body></html>',
		status=404,
	)

@app.route('/api/status')
def status():
	return flask.jsonify(_status)

def main(argv):
	"""
	The main function for the web server.
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Probe Server')
	parser.add_argument('-p', '--port', type=int, default=27182,
		help='Port to run on.')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	_backgroundUpdate()
	backgroundThread = threading.Thread(target=_backgroundThread)
	backgroundThread.daemon = True
	backgroundThread.start()

	app.run(port=arguments.port)
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))
