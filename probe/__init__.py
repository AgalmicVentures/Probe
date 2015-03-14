#!/usr/bin/env python3

import cherrypy
import sys

import application

def main():
	print('Starting up Probe...')

	cherrypy.config.update({
		'server.socket_host': '0.0.0.0',
		'server.socket_port': 27182,
	})

	probe = application.ProbeApplication()
	cherrypy.quickstart(probe)

	print('Shutting down Probe...')
	return 0

if __name__ == '__main__':
	sys.exit(main())
