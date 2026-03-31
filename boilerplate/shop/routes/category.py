from yhttp.core import json, statuscode, statuses
from sqlalchemy.exc import IntegrityError

from ...common import guard
from ...rollup import app
from ..models import Category


@app.route(r'/apiv1/categories')
@app.bodyguard((
    guard.Title('title_en'),
    guard.Title('title_fa'),
    guard.Title('title_ar'),
    guard.VectorImage('icon'),
), strict=True)
@json
@statuscode('201 Created')
def create(req):
    filename = app.media.save(req.files['icon'], 'categories')

    with app.db.session() as session:
        c = Category(
            title_en=req.form['title_en'],
            title_fa=req.form['title_fa'],
            title_ar=req.form['title_ar'],
            icon=filename,
        )
        session.add(c)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            app.media.delete(filename, 'categories')
            raise statuses.conflict()

        return c.todict()
