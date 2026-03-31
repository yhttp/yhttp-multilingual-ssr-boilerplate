from bddrest import status, response, when, given
from freezegun import freeze_time

from boilerplate.auth import basedata
from boilerplate.auth.models import Member


@freeze_time('2024-08-22')
def test_profile_get(httpreq, app):
    basedata.insert(app.db)

    # Create a token.
    with app.db.session() as session:
        god = session.query(Member).filter_by(email='god@example.com') \
            .one()
        token = god.create_token(app)

    with httpreq(path='/profiles/me', verb='GET',
                 headers={'Authorization': f'Bearer {token}'}):
        assert status == 200
        assert response.json == {
            'id': 1,
            'email': 'god@example.com',
            'nickname': 'god',
            'nickname_isdirty': True,
            'name': 'God',
            'roles': ['god'],
            'locale': 'en-US',
            'phone': None,
            'avatar': None,
            'timezone': '00:00',
            'created_at': '2024-08-22T03:30:00',
            'modified_at': '2024-08-22T03:30:00',
        }

        when(
            title='Authorization header is not passed',
            headers=given - 'Authorization'
        )
        assert status == 401

        # Delete the user
        with app.db.session() as session:
            god = session.query(Member).filter_by(email='god@example.com') \
                .delete()
            session.commit()

        when(title='User is already deleted')
        assert status == 404
