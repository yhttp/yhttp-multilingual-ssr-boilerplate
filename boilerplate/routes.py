from yhttp.core import json

from .rollup import app
from .manifest import __langs__


@app.route(r'/')
@app.bodyguard(strict=True)
@app.i18n
@app.template('index.mako')
def get(req):
    return dict(
        appname=app.name,
        version=app.version
    )


@app.route(r'/apiv1/manifest')
@app.bodyguard(strict=True)
@json
def get(req):
    return dict(
        appname=app.name,
        version=app.version,
        locales=list(__langs__.values()),
    )
