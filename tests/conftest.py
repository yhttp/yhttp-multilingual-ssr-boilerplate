import io
import uuid
import functools
import contextlib

import pytest
import bddrest
import bddcli

from yhttp.dev.fixtures import redis, freshdb, cicd, tempdir, mockupfs

import boilerplate


@pytest.fixture
def cliapp():
    cliapp = bddcli.Application('boilerplate', 'boilerplate:app.climain')
    return functools.partial(bddcli.Given, cliapp)


@pytest.fixture
def app(freshdb, redis, tempdir):
    boilerplate.app.settings.merge(f'''
      db:
        url: {freshdb}
      auth:
        token:
          secret: '12345678901234567890123456789012'
        refresh:
          secret: '12345678901234567890123456789012'
        oauth2:
          state:
            secret: '12345678901234567890123456789012'
      media:
        physical: {tempdir}
    ''')

    boilerplate.app.ready()
    boilerplate.app.db.create_objects()
    yield boilerplate.app
    boilerplate.app.shutdown()


@pytest.fixture
def httpreq(app):
    yield functools.partial(bddrest.Given, app)
    # TODO: Add documents


@pytest.fixture
def uuidfilename_patch(mocker):
    p = None

    def patch(ext):
        nonlocal p

        if p:
            p.stop()

        u = str(uuid.uuid1())
        fn = f'{u}{ext}'
        p = mocker.patch.object(uuid, 'uuid4', return_value=uuid.UUID(u))
        p.start()
        return fn

    yield patch
    p.stop()


@pytest.fixture
def memfile():
    def create(name):
        file = io.BytesIO(b'loremipsum')
        file.name = name
        return file

    yield create
