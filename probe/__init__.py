#!/usr/bin/env python3

import cherrypy
import sys

class Probe:

	def __init__(self):
		#TODO: JSON API
		#TODO: raw API
		#TODO: human interface
		pass

	@cherrypy.expose
	def index(self):
		return '<html><body><h1>Probe</h1></body></html>'

	@cherrypy.expose
	def default(self, *args, **kwargs):
		return '<html><body><h1>Probe - Page Not Found</h1></body></html>'

def main():
	print('Starting up')

	probe = Probe()
	cherrypy.quickstart(probe)

	print('Shutting down')
	return 0

if __name__ == '__main__':
	sys.exit(main())
