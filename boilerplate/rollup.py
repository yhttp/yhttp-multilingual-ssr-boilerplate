import os

from yhttp.core import Application, Request
from yhttp.ext import dbmanager, sqlalchemy as saext, auth, media, i18n, mako

from .manifest import __version__, __appname__, __langs__
from .cli import BaseDataCommand, MockupDataCommand
from .common.models import BaseModel


# find some paths
here = os.path.dirname(__file__)
prjroot = os.path.abspath(os.path.join(here, '..'))
mediaroot = os.path.join(prjroot, 'media')
staticroot = os.path.join(prjroot, 'www/static')


# create the main wsgi application
app = Application(__version__, __appname__)
app.staticdirectory('/static', staticroot)
app.staticdirectory('/media', mediaroot)


# create request rewriter to convert the leading language specifier URL part to
# HTTP Accept-Languages header.
_rewrite = i18n.create_rewriter(__langs__)


def _create_request(app, environ, response):
    _rewrite(environ)
    return Request(app, environ, response)


app.request_factory = _create_request


# Install extensions
i18n.install(app)
dbmanager.install(app, cliarguments=[
    BaseDataCommand,
    MockupDataCommand,
])
saext.install(app, basemodel=BaseModel, saplugins=['geoalchemy2'])
auth.install(app)
media.install(app)
mako.install(app, data=dict(settings=app.settings))


# Builtin settings
app.settings.merge(f'''
debug: true
production: false
www: http://localhost:5173
root: http://localhost:8080

db:
  url: postgresql://:@/{app.name}

i18n:
  domain: messages
  localedirectory: {prjroot}/i18n

media:
  physical: {mediaroot}
  virtual: /media

mako:
  modules: {prjroot}/.mako
  lookup:
    - {prjroot}/templates

oauth:
  google:
    authurl: https://accounts.google.com/o/oauth2/v2/auth
    tokenurl: https://oauth2.googleapis.com/token
    clientid: foobarbaz
    clientsecret: '12345678901234567890123456789012'

auth:
  redis:
    host: localhost
    port: 6379
    db: 0

  token:
    algorithm: HS256
    secret: '12345678901234567890123456789012'
    maxage: 3600 # seconds
    leeway: 10 # seconds

  refresh:
    key: yhttp-refresh-token
    algorithm: HS256
    secret: '12345678901234567890123456789012'
    secure: true
    httponly: true
    maxage: 2592000  # 1 Month
    leeway: 10  # seconds
    domain: example.com
    path:
    samesite: Strict

  csrf:
    key: yhttp-csrf-token
    secure: true
    httponly: true
    maxage: 60 # 1 Minute
    samesite: Strict
    domain:
    path:

  oauth2:
    state:
      algorithm: HS256
      secret: '12345678901234567890123456789012'
      maxage: 60 # 1 Minute
      leeway: 10 # seconds
''')


# Import models
from .common import models
from .auth import models
from .shop import models


# http handlers
from . import routes
from .auth import routes
from .shop import routes
