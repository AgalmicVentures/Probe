#!/usr/bin/env python3

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
