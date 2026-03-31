from yhttp.core import json, statuscode, statuses

from ...common import guard
from ...common.statuses import conflict_json
from ...rollup import app
from ..models import Good, Kind, Shop, Brand, Category


@app.route(r'/apiv1/goods/(\d+)/specifications')
@json
def update(req, id):
    with app.db.session() as session:
        g = session.get(Good, id)
        if not g:
            raise statuses.notfound()

        g.spec = req.json
        session.commit()

    return req.json


@app.route(r'/apiv1/goods/(\d+)/kinds')
@app.bodyguard((
    guard.ID('good_id'),
    guard.Title('title_en', optional=True),
    guard.Title('title_fa', optional=True),
    guard.Title('title_ar', optional=True),
    guard.PositiveInteger('price'),
    guard.PositiveInteger('count'),
    guard.BitmapImage('image', optional=True),
), strict=True)
@json
@statuscode('201 Created')
def create(req, id):
    with app.db.session() as session:
        good_id = req.form['good_id']
        if not session.get(Good, good_id):
            raise conflict_json(
                body=dict(err=f'Good doesn\'t exists: {req.form["good_id"]}')
            )

        k = Kind(
            title_en=req.form['title_en'],
            title_fa=req.form['title_fa'],
            title_ar=req.form['title_ar'],
            image=app.media.save(req.files['image'], 'goods'),
            good_id=good_id,
            price=req.form['price'],
            count=req.form['count'],
        )

        session.add(k)
        session.commit()
        return k.todict()


@app.route(r'/apiv1/goods')
@app.bodyguard((
    guard.ID('shop_id'),
    guard.ID('brand_id'),
    guard.ID('category_id'),
    guard.Title('title_en'),
    guard.Title('title_fa'),
    guard.Title('title_ar'),
    guard.Description('description_en'),
    guard.Description('description_fa'),
    guard.Description('description_ar'),
    guard.BitmapImage('image'),
), strict=True)
@json
@statuscode('201 Created')
def create(req):
    with app.db.session() as session:
        if not session.get(Shop, req.form['shop_id']):
            raise conflict_json(body=dict(
                err=f'Shop doesn\'t exists: {req.form["shop_id"]}')
            )

        if not session.get(Category, req.form['category_id']):
            raise conflict_json(body=dict(
                err=f'Category doesn\'t exists: {req.form["category_id"]}')
            )

        if not session.get(Brand, req.form['brand_id']):
            raise conflict_json(
                body=dict(err=f'Brand doesn\'t exists: {req.form["brand_id"]}')
            )

        filename = app.media.save(req.files['image'], 'goods')
        g = Good(
            shop_id=req.form['shop_id'],
            brand_id=req.form['brand_id'],
            category_id=req.form['category_id'],
            title_en=req.form['title_en'],
            title_fa=req.form['title_fa'],
            title_ar=req.form['title_ar'],

            description_en=req.form['description_en'],
            description_fa=req.form['description_fa'],
            description_ar=req.form['description_ar'],

            images=[filename],
            spec=dict(),
            kinds=[],
        )
        session.add(g)
        session.commit()
        return g.todict()
