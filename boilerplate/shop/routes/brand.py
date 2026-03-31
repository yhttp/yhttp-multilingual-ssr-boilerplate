from yhttp.core import json, statuscode, statuses
from sqlalchemy.exc import IntegrityError

from ...common import guard
from ...rollup import app
from ..models import Brand


@app.route(r'/apiv1/brands')
@app.bodyguard((
    guard.Title('title'),
    guard.VectorImage('logo'),
), strict=True)
@json
@statuscode('201 Created')
def create(req):
    filename = app.media.save(req.files['logo'], 'brands')

    with app.db.session() as session:
        c = Brand(
            title=req.form['title'],
            logo=filename,
        )
        session.add(c)

        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            app.media.delete(filename, 'brands')
            raise statuses.conflict()

        return c.todict()
