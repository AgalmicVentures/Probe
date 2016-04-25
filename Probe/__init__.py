#!/usr/bin/env python3

import cherrypy
import sys

import Application

def secureHeaders():
    cherrypy.response.headers['X-Frame-Options'] = 'DENY'
    cherrypy.response.headers['X-XSS-Protection'] = '1; mode=block'
    cherrypy.response.headers['Content-Security-Policy'] = "default-src='self'"

cherrypy.tools.secureHeaders = cherrypy.Tool('before_finalize', secureHeaders)

def main():
	print('Starting up Probe...')

	probe = Application.ProbeApplication()
	cherrypy.quickstart(probe, config='server.conf')

	print('Shutting down Probe...')
	return 0

if __name__ == '__main__':
	sys.exit(main())
