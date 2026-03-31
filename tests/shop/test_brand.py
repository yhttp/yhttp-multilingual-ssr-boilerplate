from os import path

from bddrest import status, response, when


def test_brand_create(httpreq, app, uuidfilename_patch, memfile):
    expected_filename = uuidfilename_patch('.svg')
    logo = memfile('foo.svg')
    foo = dict(
        title='Foo',
        logo=logo,
    )

    expected_brand = dict(
        id=1,
        title='Foo',
        logo=expected_filename,
    )

    with httpreq(path='/apiv1/brands', verb='CREATE', multipart=foo):
        assert status == 201
        assert response.json == expected_brand
        assert path.exists(path.join(
            app.settings.media.physical, 'brands', expected_filename))

        # duplicate title
        when()
        assert status == 409
