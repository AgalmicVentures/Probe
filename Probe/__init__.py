#!/usr/bin/env python3

import cherrypy
import sys

import Application

def main():
	print('Starting up Probe...')

	probe = Application.ProbeApplication()
	cherrypy.quickstart(probe, config='server.conf')

	print('Shutting down Probe...')
	return 0

if __name__ == '__main__':
	sys.exit(main())
