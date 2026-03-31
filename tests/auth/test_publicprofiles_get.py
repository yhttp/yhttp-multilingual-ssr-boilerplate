from bddrest import status, response, when, given
from freezegun import freeze_time

from boilerplate.auth import basedata
from boilerplate.auth.models import Member


@freeze_time('2024-08-23')
def test_publicprofiles_get(httpreq, app):
    basedata.insert(app.db)

    # Create a token.
    with app.db.session() as session:
        admin = session.query(Member).filter_by(email='admin@example.com') \
            .one()
        token = admin.create_token(app)

    with httpreq(
        path='/publicprofiles',
        verb='GET',
        headers={
            'Authorization': f'Bearer {token}'
        },
        query=dict(email='admin@example.com')
    ):
        assert status == 200
        assert response.json == [{
            'nickname': 'admin',
            'avatar': None
        }]

        when(query=dict(email='iamnotarealuser@example.com'))
        assert status == 200
        assert response.json == []

        when(query=given - 'email')
        assert status == '400 email: Required'

        # SQL Injection Attack! ORM must handle it!
        when(query=dict(email='whatever\' or 1=1'))
        assert status == '400 email: Invalid Format'
