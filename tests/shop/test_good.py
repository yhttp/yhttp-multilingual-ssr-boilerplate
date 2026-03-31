from os import path

import pytest
from bddrest import status, response, when, given

from boilerplate.common.models import City
from boilerplate.shop.models import ShopType, Shop, Category, Brand


@pytest.fixture
def mockup(app):
    with app.db.session() as session:
        city = City(
            title_en='corge en',
            title_fa='corge fa',
            title_ar='corge ar',
        )
        shop = Shop(title='Quux', type=ShopType.STORE, city_id=1)
        brand = Brand(title='Thud', logo='thud.svg')
        category = Category(
            title_en='Qux en',
            title_fa='Qux fa',
            title_ar='Qux ar',
            icon='qux.svg',
        )

        session.add(city)
        session.add(shop)
        session.add(brand)
        session.add(category)
        session.commit()


def test_good_create_errors(httpreq, app):
    with httpreq(path='/apiv1/goods', verb='CREATE', form=dict()):
        assert status == 400

    with httpreq(path='/apiv1/goods', verb='CREATE', multipart=dict()):
        assert status == 400


def test_good_create(httpreq, app, mockup, uuidfilename_patch, memfile):
    expected_filename = uuidfilename_patch('.jpg')
    image = memfile('foo.jpg')
    foo = dict(
        shop_id=1,
        category_id=1,
        brand_id=1,
        title_en='Foo en',
        title_fa='Foo fa',
        title_ar='Foo ar',
        description_en='lorem ipsum en',
        description_fa='lorem ipsum fa',
        description_ar='lorem ipsum ar',
        image=image,
    )

    expected_good = dict(
        id=1,
        title_en='Foo en',
        title_fa='Foo fa',
        title_ar='Foo ar',
        description_en='lorem ipsum en',
        description_fa='lorem ipsum fa',
        description_ar='lorem ipsum ar',
        images=[expected_filename],
        spec=dict(),
    )

    # create a good
    with httpreq(path='/apiv1/goods', verb='CREATE', multipart=foo):
        assert status == 201
        assert response.json == expected_good
        assert path.exists(
            path.join(app.settings.media.physical, 'goods', expected_filename))

        when(multipart=given | dict(brand_id=2))
        assert status == 409
        assert response.json == dict(err='Brand doesn\'t exists: 2')

        when(multipart=given | dict(shop_id=2))
        assert status == 409
        assert response.json == dict(err='Shop doesn\'t exists: 2')

        when(multipart=given | dict(category_id=2))
        assert status == 409
        assert response.json == dict(err='Category doesn\'t exists: 2')

    # update specifictions
    spec = dict(foo='bar', baz=2)
    with httpreq(path='/apiv1/goods/id: 1/specifications',
                 verb='UPDATE', json=spec):
        assert status == 200
        assert response.json == spec

        when(path_parameters=given | dict(id=2))
        assert status == 404

    # kinds
    kind = dict(
        good_id=1,
        title_en='bar en',
        title_fa='bar fa',
        title_ar='bar ar',
        price=100,
        count=10,
        image=memfile('bar.png'),
    )
    expected_kind = dict(
        id=1,
        good_id=1,
        title_en='bar en',
        title_fa='bar fa',
        title_ar='bar ar',
        price=100,
        count=10,
        image=uuidfilename_patch('.png'),
    )

    with httpreq(path='/apiv1/goods/id: 1/kinds', verb='CREATE',
                 multipart=kind):
        assert status == 201
        assert response.json == expected_kind

        when(multipart=given | dict(good_id=2))
        assert status == 409
        assert response.json == dict(err='Good doesn\'t exists: 2')
