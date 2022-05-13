#!/usr/bin/python3

from wsgiref.handlers import CGIHandler

from main import app

class ProxyFix(object):
   def __init__(self, app):
      self.app = app

   def __call__(self, environ, start_response):
      return self.app(environ, start_response)

if __name__ == '__main__':
  app.wsgi_app = ProxyFix(app.wsgi_app)
  CGIHandler().run(app)
