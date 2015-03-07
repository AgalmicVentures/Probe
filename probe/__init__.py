#!/usr/bin/env python3

import cherrypy
import sys

import application

def main():
	print('Starting up')

	probe = application.ProbeApplication()
	cherrypy.quickstart(probe)

	print('Shutting down')
	return 0

if __name__ == '__main__':
	sys.exit(main())
