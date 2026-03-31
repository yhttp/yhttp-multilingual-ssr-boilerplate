from os import path

from bddrest import status, response, when


def test_category_create(httpreq, app, uuidfilename_patch, memfile):
    expected_filename = uuidfilename_patch('.svg')
    icon = memfile('foo.svg')
    foo = dict(
        title_en='Foo en',
        title_fa='Foo fa',
        title_ar='Foo ar',
        icon=icon,
    )

    expected_category = dict(
        id=1,
        title_en='Foo en',
        title_fa='Foo fa',
        title_ar='Foo ar',
        icon=expected_filename,
    )

    with httpreq(path='/apiv1/categories', verb='CREATE', multipart=foo):
        assert status == 201
        assert response.json == expected_category
        assert path.exists(path.join(
            app.settings.media.physical, 'categories', expected_filename))

        # duplicate title
        when()
        assert status == 409
