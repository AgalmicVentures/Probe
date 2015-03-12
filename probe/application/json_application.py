
import cherrypy
from datetime import datetime
import json
import psutil

class ProbeJsonApplication:

	def __init__(self):
		pass

	@cherrypy.expose
	def default(self, *args, **kwargs):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'error': 'API not found',
		}).encode('utf8')

	@cherrypy.expose
	def hardware(self):
		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'bootTime': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S'),
			'cpuCores': psutil.NUM_CPUS,
			'ram': psutil.TOTAL_PHYMEM,
		}, indent=4, sort_keys=True).encode('utf8')

	@cherrypy.expose
	def status(self):
		bootTime = datetime.fromtimestamp(psutil.boot_time())
		now = datetime.now()

		virtualMemory = psutil.virtual_memory()
		swapMemory = psutil.swap_memory()
		network = psutil.net_io_counters()

		cherrypy.response.headers['Content-Type'] = 'application/json'
		return json.dumps({
			'time': now.strftime('%Y-%m-%d %H:%M:%S'),
			'uptime': int((now - bootTime).total_seconds()),
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
		}, indent=4, sort_keys=True).encode('utf8')
