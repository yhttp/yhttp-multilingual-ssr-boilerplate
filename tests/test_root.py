from bddrest import status, response


def test_root_get(httpreq, app):
    with httpreq('/'):
        assert status == 200


def test_manifest_get(httpreq, app):
    with httpreq('/apiv1/manifest'):
        assert status == 200
        assert response.json == dict(
            appname=app.name,
            version=app.version,
            locales=['en_US', 'fa_IR', 'ar_OM'],
        )
